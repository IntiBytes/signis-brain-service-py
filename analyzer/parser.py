

def parse_robots(content: str) -> dict:
    lines = content.splitlines()
    groups = {}
    current_agents = []
    sitemaps = []


    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            continue


        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()

        if key == "user-agent":
            current_agents.append(value)
        elif key == "sitemap":
            if value:
                sitemaps.append(value)
        elif key in ["disallow", "allow", "crawl-delay"]:
            for agent in current_agents:
                if agent not in groups:
                    groups[agent] = {"disallow": [], "allow": [], "crawl_delay": None}
                
                if key == "disallow":
                    if value: groups[agent]["disallow"].append(value)
                elif key == "allow":
                    if value: groups[agent]["allow"].append(value)
                elif key == "crawl-delay":
                    groups[agent]["crawl_delay"] = value
        
       
        if key not in ["user-agent"]:
            pass

    if "*" not in groups:
        groups["*"] = {"disallow": [], "allow": [], "crawl_delay": None}

    return {"groups": groups, "sitemaps": sitemaps}