import os
from models.schemas import BrainRequest, AgentRules

AI_BOTS = os.getenv("AI_BOTS_LIST", "").split(",")

def score_robots(parsed: BrainRequest) ->  tuple[int: str]:
    score = 100
    groups = parsed.groups
    sitemaps = parsed.sitemaps

    # 1. Sitemap Penalty (Critical for discovery)
    if not sitemaps:
        score -= 25

    # 2. Wildcard Block Penalty (The "Nuclear" option)
    _empty = AgentRules(allow=[], disallow=[])
    wildcard = groups.get("*", _empty)
    if "/" in wildcard.disallow:
        score -= 40

    # 3. AI Bot Specific Penalties + Omission Penalty
    blocked_ai_count = 0
    found_ai_bots = [bot for bot in AI_BOTS if bot in groups]

    # Penalty for omission: no AI bot rules at all = not "AI-Proactive"
    if len(found_ai_bots) == 0:
        score -= 12  # Aligns score with stricter AI-audit tools (e.g. 100 - 25 - 12 = 63)

    for bot in AI_BOTS:
        bot_rules = groups.get(bot, _empty)
        # Check if explicitly blocked or inherited from wildcard block
        is_blocked = "/" in bot_rules.disallow or ("/" in wildcard.disallow and bot not in groups)
      
        if is_blocked:
            blocked_ai_count += 1
            score -= 10 # -10 per blocked major AI bot

    # 4. Crawl Delay Penalty (AI bots hate waiting)
    for agent, rules in groups.items():
        if rules.crawl_delay:
            try:
                if int(rules.crawl_delay) > 5:
                    score -= 5
            except:
                pass

    score = max(0, min(100, score))

    if score >= 85: verdict = "excellent"
    elif score >= 65: verdict = "good"
    elif score >= 40: verdict = "fair"
    else: verdict = "poor"

    return score, verdict