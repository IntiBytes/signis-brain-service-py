from models.schemas import BrainRequest, BrainStats, BrainMeta
from analyzer.normalizer import normalize_groups


def compute_stats(parsed: BrainRequest) -> tuple[BrainStats, BrainMeta]:
    groups = normalize_groups(parsed.groups)
    sitemaps = parsed.sitemaps

    total_allow = sum(len(r.allow) for r in groups.values())
    total_disallow = sum(len(r.disallow) for r in groups.values())
    total_crawl_delay = sum(
        len(r.crawl_delay) for r in groups.values() if r.crawl_delay is not None
    )
    has_crawl_delay = total_crawl_delay > 0
    rules_count = total_allow + total_disallow + len(sitemaps) + total_crawl_delay
    has_sitemap = len(sitemaps) > 0
    agents = len(groups)

    return (
        BrainStats(
            user_agents=agents,
            allow_rules=total_allow,
            disallow_rules=total_disallow,
            crawl_delay_rules=total_crawl_delay,
            has_sitemap=has_sitemap,
            has_crawl_delay=has_crawl_delay,
        ),
        BrainMeta(
            agents=list(groups.keys()),
            parsed_warnings=None,
            parsed_issues=None,
            parsed_good_practices=None,
            rules_count=rules_count,
        ),
    )
