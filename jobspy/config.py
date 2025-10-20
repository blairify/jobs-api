# ========================================
# Configuration groups for different job categories
# ========================================

# --- Base parameters ---
DEFAULT_SITES = ["linkedin", "indeed"]
DEFAULT_RESULTS = 50
DEFAULT_HOURS = 72
DEFAULT_DELAY = 3

# --- Software Engineering ---
SOFTWARE_ENGINEERING_CONFIGS = [
    # United States (nationwide + major cities)
    {"query_id": "software_engineer_usa", "search_term": "software engineer", "location": "United States"},
    {"query_id": "software_engineer_sf", "search_term": "software engineer", "location": "San Francisco, CA"},
    {"query_id": "software_engineer_ny", "search_term": "software engineer", "location": "New York, NY"},
    {"query_id": "software_engineer_austin", "search_term": "software engineer", "location": "Austin, TX"},
    {"query_id": "software_engineer_seattle", "search_term": "software engineer", "location": "Seattle, WA"},
    {"query_id": "junior_software_engineer", "search_term": "junior software engineer", "location": "United States", "results_wanted": 50},
    {"query_id": "software_engineer_intern", "search_term": "software engineer intern", "location": "United States", "hours_old": 168, "delay": 2},

    # International
    {"query_id": "software_engineer_warsaw", "search_term": "software engineer", "location": "Warsaw, Poland"},
    {"query_id": "software_engineer_london", "search_term": "software engineer", "location": "London, United Kingdom"},
    {"query_id": "software_engineer_berlin", "search_term": "software engineer", "location": "Berlin, Germany"},
    {"query_id": "software_engineer_paris", "search_term": "software engineer", "location": "Paris, France"},
    {"query_id": "software_engineer_bangalore", "search_term": "software engineer", "location": "Bangalore, India"},
    {"query_id": "software_engineer_singapore", "search_term": "software engineer", "location": "Singapore"},
    {"query_id": "software_engineer_sydney", "search_term": "software engineer", "location": "Sydney, Australia"}
]

# --- Data Science & AI ---
DATA_SCIENCE_CONFIGS = [
    # Remote and U.S. searches
    {"query_id": "python_developer_remote", "search_term": "python developer", "location": "Remote"},
    {"query_id": "data_scientist_usa", "search_term": "data scientist", "location": "United States"},
    {"query_id": "data_engineer_usa", "search_term": "data engineer", "location": "United States"},
    {"query_id": "machine_learning_engineer_usa", "search_term": "machine learning engineer", "location": "United States"},

    # Major U.S. cities
    {"query_id": "data_scientist_sf", "search_term": "data scientist", "location": "San Francisco, CA"},
    {"query_id": "data_scientist_ny", "search_term": "data scientist", "location": "New York, NY"},
    {"query_id": "data_scientist_austin", "search_term": "data scientist", "location": "Austin, TX"},
    {"query_id": "data_scientist_seattle", "search_term": "data scientist", "location": "Seattle, WA"},

    # Canada
    {"query_id": "data_scientist_toronto", "search_term": "data scientist", "location": "Toronto, Canada"},
    {"query_id": "data_scientist_vancouver", "search_term": "data scientist", "location": "Vancouver, Canada"},

    # Europe
    {"query_id": "data_scientist_london", "search_term": "data scientist", "location": "London, United Kingdom"},
    {"query_id": "data_scientist_berlin", "search_term": "data scientist", "location": "Berlin, Germany"},
    {"query_id": "data_scientist_paris", "search_term": "data scientist", "location": "Paris, France"},
    {"query_id": "data_scientist_warsaw", "search_term": "data scientist", "location": "Warsaw, Poland"},

    # Asia
    {"query_id": "data_scientist_bangalore", "search_term": "data scientist", "location": "Bangalore, India"},
    {"query_id": "data_scientist_mumbai", "search_term": "data scientist", "location": "Mumbai, India"},
    {"query_id": "data_scientist_singapore", "search_term": "data scientist", "location": "Singapore"},

    # Australia
    {"query_id": "data_scientist_sydney", "search_term": "data scientist", "location": "Sydney, Australia"},
    {"query_id": "data_scientist_melbourne", "search_term": "data scientist", "location": "Melbourne, Australia"},

    # Entry-level & Analyst roles
    {"query_id": "junior_data_scientist", "search_term": "junior data scientist", "location": "United States"},
    {"query_id": "data_analyst_global", "search_term": "data analyst", "location": "Worldwide"}
]

# --- Web Development ---
WEB_DEVELOPMENT_CONFIGS = [
    {"query_id": "frontend_developer", "search_term": "frontend developer", "location": "United States"},
    {"query_id": "backend_developer", "search_term": "backend developer", "location": "United States"},
    {"query_id": "fullstack_developer", "search_term": "full stack developer", "location": "United States"},
    {"query_id": "frontend_developer_london", "search_term": "frontend developer", "location": "London, United Kingdom"},
    {"query_id": "frontend_developer_bangalore", "search_term": "frontend developer", "location": "Bangalore, India"}
]

# --- DevOps & Cloud ---
DEVOPS_CLOUD_CONFIGS = [
    {"query_id": "devops_engineer_usa", "search_term": "devops engineer", "location": "United States"},
    {"query_id": "cloud_engineer_usa", "search_term": "cloud engineer", "location": "United States"},
    {"query_id": "aws_engineer_usa", "search_term": "aws engineer", "location": "United States", "results_wanted": 80},
    {"query_id": "devops_engineer_london", "search_term": "devops engineer", "location": "London, United Kingdom"},
    {"query_id": "cloud_engineer_bangalore", "search_term": "cloud engineer", "location": "Bangalore, India"}
]

# --- Specialized Roles ---
SPECIALIZED_CONFIGS = [
    {"query_id": "ios_developer", "search_term": "ios developer", "location": "United States", "results_wanted": 80},
    {"query_id": "android_developer", "search_term": "android developer", "location": "United States", "results_wanted": 80},
    {"query_id": "security_engineer", "search_term": "security engineer", "location": "United States", "results_wanted": 80},
    {"query_id": "blockchain_developer", "search_term": "blockchain developer", "location": "United States"},
    {"query_id": "cybersecurity_analyst", "search_term": "cybersecurity analyst", "location": "United States"},
    {"query_id": "ai_research_engineer", "search_term": "ai research engineer", "location": "Worldwide"}
]

# --- Apply defaults ---
def apply_defaults(configs):
    for cfg in configs:
        cfg.setdefault("site_name", DEFAULT_SITES)
        cfg.setdefault("results_wanted", DEFAULT_RESULTS)
        cfg.setdefault("hours_old", DEFAULT_HOURS)
        cfg.setdefault("delay", DEFAULT_DELAY)
    return configs

SOFTWARE_ENGINEERING_CONFIGS = apply_defaults(SOFTWARE_ENGINEERING_CONFIGS)
DATA_SCIENCE_CONFIGS = apply_defaults(DATA_SCIENCE_CONFIGS)
WEB_DEVELOPMENT_CONFIGS = apply_defaults(WEB_DEVELOPMENT_CONFIGS)
DEVOPS_CLOUD_CONFIGS = apply_defaults(DEVOPS_CLOUD_CONFIGS)
SPECIALIZED_CONFIGS = apply_defaults(SPECIALIZED_CONFIGS)

# --- Combined for backward compatibility ---
SEARCH_CONFIGS = (
    SOFTWARE_ENGINEERING_CONFIGS +
    DATA_SCIENCE_CONFIGS +
    WEB_DEVELOPMENT_CONFIGS +
    DEVOPS_CLOUD_CONFIGS +
    SPECIALIZED_CONFIGS
)

# --- Workflow selection mapping ---
CONFIG_GROUPS = {
    "software_engineering": SOFTWARE_ENGINEERING_CONFIGS,
    "data_science": DATA_SCIENCE_CONFIGS,
    "web_development": WEB_DEVELOPMENT_CONFIGS,
    "devops_cloud": DEVOPS_CLOUD_CONFIGS,
    "specialized": SPECIALIZED_CONFIGS,
    "all": SEARCH_CONFIGS
}
