from analyzer.normalizer import normalize_groups, normalize_bot_name
from models.schemas import BrainRequest, AgentRules
from utils.ai import AI_BOTS


def score_robots(parsed: BrainRequest) -> tuple[int:str]:
    score = 100
    _empty = AgentRules(allow=[], disallow=[])
    sitemaps = parsed.sitemaps

    # Normalize all group keys
    groups = normalize_groups(parsed.groups)
    wildcard = groups.get("*", _empty)

    # 1. Sitemap Penalty (Critical for discovery)
    if not sitemaps:
        score -= 25

    # 2. Wildcard Block Penalty (The "Nuclear" option)
    if "/" in wildcard.disallow:
        score -= 40

    # 3. AI Bot Specific Penalties + Omission Penalty
    found_ai_bots = [bot for bot in AI_BOTS if bot in groups]

    # Penalty for omission: no AI bot rules at all = not "AI-Proactive"
    if len(found_ai_bots) == 0:
        score -= (
            12  # Aligns score with stricter AI-audit tools (e.g. 100 - 25 - 12 = 63)
        )

    # 4. Explicit Block Penalty (AI bots hate being blocked)
    for bot in AI_BOTS:
        bot_key = normalize_bot_name(bot)
        bot_rules = groups.get(bot_key, _empty)
        # Check if explicitly blocked or inherited from wildcard block
        is_blocked = "/" in bot_rules.disallow or (
            "/" in wildcard.disallow and bot_key not in groups
        )

        if is_blocked:
            score -= 10  # -10 per blocked major AI bot

    # 5. Crawl Delay Penalty (AI bots hate waiting)
    for agent, rules in groups.items():
        if rules.crawl_delay:
            try:
                if int(rules.crawl_delay) > 5:
                    score -= 5
            except ValueError:
                print(f"Invalid crawl delay for {agent}: {rules.crawl_delay}")
                pass

    score = max(0, min(100, score))

    if score >= 85:
        verdict = "excellent"
    elif score >= 65:
        verdict = "good"
    elif score >= 40:
        verdict = "fair"
    else:
        verdict = "poor"

    return score, verdict
