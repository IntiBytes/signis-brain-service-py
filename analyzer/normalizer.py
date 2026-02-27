from models.schemas import AgentRules
from typing import Dict

def normalize_groups(groups: Dict[str, AgentRules]) -> Dict[str, AgentRules]:
    """
    Normalize all agent keys to lowercase and strip surrounding quotes/spaces.
    This prevents false 'No explicit rule for X' recommendations when the bot
    IS present but with different casing or extra characters.

    e.g: '"GPTBot"' -> 'gptbot'
         ' ClaudeBot ' -> 'claudebot'
    """
    return {normalize_bot_name(agent): rules for agent, rules in groups.items()}

def normalize_bot_name(bot_name: str) -> str:
    return bot_name.strip().lower().strip('"') 