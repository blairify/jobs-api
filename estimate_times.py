#!/usr/bin/env python3
"""Estimate workflow execution times"""

# Read and execute the config file directly
with open('/Users/mati/Documents/code/freelance/jobs-api/jobspy/config.py', 'r') as f:
    config_code = f.read()

exec(config_code)

# Estimate time per query (scraping + delay)
# Assuming ~30-60 seconds per query on average (scraping time varies)
# Plus the configured delay (3 seconds default)
AVG_SCRAPE_TIME = 45  # seconds per query (conservative estimate)
DELAY = 3  # seconds between queries

TIME_PER_QUERY = AVG_SCRAPE_TIME + DELAY  # ~48 seconds total

print("=" * 70)
print("WORKFLOW TIMEOUT RISK ANALYSIS")
print("=" * 70)
print(f"\nAssumptions:")
print(f"  - Average scrape time: {AVG_SCRAPE_TIME}s per query")
print(f"  - Delay between queries: {DELAY}s")
print(f"  - Total time per query: {TIME_PER_QUERY}s (~{TIME_PER_QUERY/60:.1f} minutes)")
print("\n" + "=" * 70)

workflows = {
    "Software Engineering": {
        "groups": ["se_general_us", "se_entry", "se_mid", "se_senior", "se_lead_architect", "se_international"],
        "timeout": 45
    },
    "Web Development": {
        "groups": ["frontend", "backend", "fullstack"],
        "timeout": 25
    },
    "Data Science": {
        "groups": ["data_science", "data_engineering", "data_analytics", "ml_ai"],
        "timeout": 30
    },
    "DevOps & Cloud": {
        "groups": ["devops", "cloud"],
        "timeout": 20
    },
    "Specialized": {
        "groups": ["mobile", "qa_testing", "security", "database", "product_project", 
                   "design", "systems_network", "emerging_tech", "remote", "internship_entry"],
        "timeout": 30
    }
}

print("\nWORKFLOW ANALYSIS:\n")

risky_workflows = []

for workflow_name, config in workflows.items():
    total_queries = sum(len(CONFIG_GROUPS[g]) for g in config["groups"])
    estimated_time = (total_queries * TIME_PER_QUERY) / 60  # in minutes
    timeout = config["timeout"]
    buffer = timeout - estimated_time
    risk_level = "🔴 HIGH RISK" if buffer < 5 else "🟡 MODERATE" if buffer < 10 else "🟢 SAFE"
    
    print(f"{workflow_name}:")
    print(f"  Queries: {total_queries}")
    print(f"  Estimated time: {estimated_time:.1f} minutes")
    print(f"  Timeout: {timeout} minutes")
    print(f"  Buffer: {buffer:.1f} minutes")
    print(f"  Status: {risk_level}")
    
    if buffer < 10:
        risky_workflows.append({
            "name": workflow_name,
            "queries": total_queries,
            "estimated": estimated_time,
            "timeout": timeout,
            "groups": config["groups"]
        })
    print()

if risky_workflows:
    print("=" * 70)
    print("RECOMMENDED ACTIONS")
    print("=" * 70)
    print("\nWorkflows that need splitting:\n")
    
    for wf in risky_workflows:
        print(f"{wf['name']}:")
        print(f"  Current: {wf['queries']} queries in {wf['timeout']} min timeout")
        print(f"  Estimated: {wf['estimated']:.1f} minutes")
        print(f"  Groups: {', '.join(wf['groups'])}")
        
        # Suggest split
        if len(wf['groups']) > 1:
            mid = len(wf['groups']) // 2
            group1 = wf['groups'][:mid]
            group2 = wf['groups'][mid:]
            queries1 = sum(len(CONFIG_GROUPS[g]) for g in group1)
            queries2 = sum(len(CONFIG_GROUPS[g]) for g in group2)
            time1 = (queries1 * TIME_PER_QUERY) / 60
            time2 = (queries2 * TIME_PER_QUERY) / 60
            
            print(f"\n  Suggested split:")
            print(f"    Part 1: {', '.join(group1)} ({queries1} queries, ~{time1:.1f} min)")
            print(f"    Part 2: {', '.join(group2)} ({queries2} queries, ~{time2:.1f} min)")
        print()
