from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# class AnalyzerRequest(BaseModel):
#     content: str
#     source_url: Optional[str] = None

# class Recommendation(BaseModel):
#     category: str
#     severity: str
#     title: str
#     suggestion: str

# class AnalyzerResponse(BaseModel):
#     score: int
#     verdict: str
#     recommendations: List[Recommendation]
#     parsed: Dict[str, Any]

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

class BrainResponse(BaseModel):
    score: int
    verdict: str
    recommendations: List[BrainRecommendation]