from typing import List, Dict, Optional
from pydantic import BaseModel


class AgentRules(BaseModel):
    allow: List[str]
    disallow: List[str]
    crawl_delay: Optional[int] = None


class BrainRequest(BaseModel):
    groups: Dict[str, AgentRules]
    sitemaps: List[str]
    source_url: Optional[str] = None


class BrainRecommendation(BaseModel):
    id: str
    type: str
    title: str
    message: str
    priority: str


class BrainStats(BaseModel):
    user_agents: int
    allow_rules: int
    disallow_rules: int
    crawl_delay_rules: int
    has_sitemap: bool
    has_crawl_delay: bool


class BrainMeta(BaseModel):
    agents: List[str]
    parsed_warnings: Optional[List[str]]
    parsed_issues: Optional[List[str]]
    parsed_good_practices: Optional[List[str]]
    rules_count: int


class BrainResponse(BaseModel):
    score: int
    verdict: str
    warnings: Optional[List[str]]
    issues: Optional[List[str]]
    recommendations: List[BrainRecommendation]
    good_practices: Optional[List[str]]
    stats: BrainStats
    meta: BrainMeta
