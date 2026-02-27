from analyzer.normalizer import normalize_groups, normalize_bot_name
from models.schemas import BrainRecommendation
from models.schemas import BrainRequest, AgentRules
from utils.ai import AI_BOTS


def generate_recommendations(
    parsed: BrainRequest,
) -> tuple[list[BrainRecommendation], list[str], list[str], list[str]]:
    """
    Returns: (recommendations, issues, warnings, good practices)
    """

    recommendations = []
    issues = []
    warnings = []
    good_practices = []

    sitemaps = parsed.sitemaps
    _empty = AgentRules(allow=[], disallow=[], crawl_delay=None)

    # * Normalize all group keys
    groups = normalize_groups(parsed.groups)
    wildcard = groups.get("*", _empty)

    # Sitemap Recs
    if not sitemaps:
        issues.append("No sitemap directives found.")
        recommendations.append(
            BrainRecommendation(
                id="sitemap-missing",
                type="critical",
                title="Missing Sitemap Directive",
                message="Add 'Sitemap: https://yourdomain.com/sitemap.xml' to help AI agents index your latest content.",
                priority="high",
            )
        )

    else:
        good_practices.append(f"Sitemap directives found: {sitemaps[0]}")

    # Wildcard Recs
    if "/" in wildcard.disallow:
        issues.append(
            "Global disallow detected '/' blocks all cralwers including AI agents."
        )
        recommendations.append(
            BrainRecommendation(
                id="global-block",
                type="general",
                title="Global Block Detected",
                message="Your robots.txt blocks all crawlers from your entire site. This prevents AI discovery. Please Remove 'Disallow: /' or scope it to specific paths.",
                priority="hihg",
            )
        )
    else:
        good_practices.append("Wildcard User-agent '*' is present (baseline coverage).")

    # * ---- AI BOTS RuLES ----- *
    found_ai_bots = [bot for bot in AI_BOTS if normalize_bot_name(bot) in groups]

    if len(found_ai_bots) == 0 and "/" not in wildcard.disallow:
        recommendations.append(
            BrainRecommendation(
                id="no-ai-agents",
                type="info",
                title="No AI Crawler Rules",
                message=f"Consider adding explicit rules for AI crawlers ({', '.join(AI_BOTS[:4])}, etc.) to signal AI-friendliness.",
                priority="low",
            )
        )
    else:
        good_practices.append(
            f"Explicit AI bot rules found for: {', '.join(found_ai_bots)}."
        )

    # AI Bot Recs
    for bot in AI_BOTS:
        bot_key = normalize_bot_name(bot)
        bot_rules = groups.get(bot_key, _empty)

        is_explicitly_blocked = "/" in bot_rules.disallow
        is_inherited_blocked = "/" in wildcard.disallow and bot_key not in groups
        is_explicitly_allowed = "/" in bot_rules.allow or "" in bot_rules.allow

        if is_explicitly_blocked:
            warnings.append(f"{bot} is explicitly blocked.")
            recommendations.append(
                BrainRecommendation(
                    id=f"ai-block-{bot}",
                    type="ai_optimization",
                    title=f"Explicit block for {bot}",
                    message=f"Remove the Disallow rule for {bot} to allow AI models to learn from your public data.",
                    priority="warning",
                )
            )
        elif is_inherited_blocked:
            warnings.append(f"{bot} is inherited blocked.")
            recommendations.append(
                BrainRecommendation(
                    id=f"ai-inherited-block-{bot}",
                    type="ai_optimization",
                    title=f"Inherited block for {bot}",
                    message=f"Remove the Disallow rule for {bot} to allow AI models to learn from your public data.",
                    priority="warning",
                )
            )
        elif not is_explicitly_allowed:
            good_practices.append(f"{bot} is explicitly allowed.")
        elif bot_key in groups:
            good_practices.append(f"{bot} has custom rules defined.")

    # Crawl Delay Recs
    for agent, rules in groups.items():
        if rules.crawl_delay:
            try:
                delay = int(rules.crawl_delay)
                if delay > 5:
                    warnings.append(
                        f"High crawl-delay ({delay}s) for '{agent}' may slow AI indexing."
                    )
                    recommendations.append(
                        BrainRecommendation(
                            id=f"high-crawl-delay-{agent}",
                            type="warning",
                            title=f"High Crawl-Delay for {agent}",
                            message=f"Crawl-delay of {delay}s is high. Consider reducing it to 5s or less for better AI crawl efficiency.",
                            priority="medium",
                        )
                    )
            except ValueError:
                print(f"Invalid crawl delay for {agent}: {rules.crawl_delay}")
                pass

    # --- Wildcard Allow-Only -----
    if wildcard.allow and not wildcard.disallow:
        warnings.append(
            "Agent '*': Has Allow rules but no Disallow rules (may be fine, but often unintended)."
        )
        recommendations.append(
            BrainRecommendation(
                id="allow-without-disallow",
                type="warning",
                title="Unusual Rules for '*'",
                message="Agent '*' has Allow rules but no Disallow rules. This may be unintended.",
                priority="medium",
            )
        )

    return recommendations, issues, warnings, good_practices
