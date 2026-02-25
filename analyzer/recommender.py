from models.schemas import BrainRecommendation
from models.schemas import BrainRequest, AgentRules
import os 

AI_BOTS = os.getenv("AI_BOTS_LIST", "").split(",")

def generate_recommendations(parsed: BrainRequest) -> BrainRecommendation:
    recs = []
    groups = parsed.groups
    sitemaps = parsed.sitemaps
    _empty = AgentRules(allow=[], disallow=[])
    wildcard = groups.get("*", _empty)

    # Sitemap Recs
    if not sitemaps:
        recs.append(BrainRecommendation(
            id="sitemap-missing",
            type="sitemap",
            title="Missing Sitemap Directive",
            message="Add 'Sitemap: https://yourdomain.com/sitemap.xml' to help AI agents index your latest content.",
            priority="critical"
        ))

    # Wildcard Recs
    if "/" in wildcard.disallow:
        recs.append(BrainRecommendation(
            id="global-block",
            type="general",
            title="Global Block Detected",
            message="Your robots.txt blocks all crawlers from your entire site. This prevents AI discovery.",
            priority="critical"
        ))

    # AI Bot Recs
    for bot in AI_BOTS:
        bot_rules = groups.get(bot, _empty)
        if "/" in bot_rules.disallow:
            recs.append(BrainRecommendation(
                id=f"ai-block-{bot}",
                type="ai_optimization",
                title=f"Explicit block for {bot}",
                message=f"Remove the Disallow rule for {bot} to allow AI models to learn from your public data.",
                priority="warning"
            ))
        elif bot not in groups and "/" not in wildcard.disallow:
            recs.append(BrainRecommendation(
                id=f"ai-allow-{bot}",
                type="ai_optimization",
                title=f"No explicit rule for {bot}",
                message=f"Add 'User-agent: {bot} \\nAllow: /' to explicitly welcome this AI agent.",
                priority="info"
            ))

    return recs