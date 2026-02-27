import os

AI_BOTS = [
    b.strip()
    for b in os.getenv(
        "AI_BOTS_LIST",
        "GPTBot,ChatGPT-User,ClaudeBot,PerplexityBot,Googlebot-Extended,CCBot,anthropic-ai",
    ).split(",")
    if b.strip()
]
