# Configuration groups for different job categories
SOFTWARE_ENGINEERING_CONFIGS = [
    {
        "query_id": "software_engineer_usa",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_sf",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_ny",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer",
        "location": "New York, NY",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_austin",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer",
        "location": "Austin, TX",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_seattle",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer",
        "location": "Seattle, WA",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "junior_software_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "junior software engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_intern",
        "site_name": ["linkedin", "indeed"],
        "search_term": "software engineer intern",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 168,
        "delay": 2
    }
]

DATA_SCIENCE_CONFIGS = [
    {
        "query_id": "python_developer_remote",
        "site_name": ["linkedin", "indeed"],
        "search_term": "python developer",
        "location": "Remote",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "data_engineer_usa",
        "site_name": ["linkedin", "indeed"],
        "search_term": "data engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "data_scientist_usa",
        "site_name": ["linkedin", "indeed"],
        "search_term": "data scientist",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "machine_learning_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "machine learning engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    }
]

WEB_DEVELOPMENT_CONFIGS = [
    {
        "query_id": "frontend_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "frontend developer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "backend_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "backend developer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "fullstack_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "full stack developer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    }
]

DEVOPS_CLOUD_CONFIGS = [
    {
        "query_id": "devops_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "devops engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "cloud_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "cloud engineer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "aws_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "aws engineer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    }
]

SPECIALIZED_CONFIGS = [
    {
        "query_id": "ios_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "ios developer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "android_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "android developer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "security_engineer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "security engineer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "blockchain_developer",
        "site_name": ["linkedin", "indeed"],
        "search_term": "blockchain developer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    }
]

# Combined configs for backward compatibility
SEARCH_CONFIGS = (
    SOFTWARE_ENGINEERING_CONFIGS +
    DATA_SCIENCE_CONFIGS +
    WEB_DEVELOPMENT_CONFIGS +
    DEVOPS_CLOUD_CONFIGS +
    SPECIALIZED_CONFIGS
)

# Config groups mapping for workflow selection
CONFIG_GROUPS = {
    "software_engineering": SOFTWARE_ENGINEERING_CONFIGS,
    "data_science": DATA_SCIENCE_CONFIGS,
    "web_development": WEB_DEVELOPMENT_CONFIGS,
    "devops_cloud": DEVOPS_CLOUD_CONFIGS,
    "specialized": SPECIALIZED_CONFIGS,
    "all": SEARCH_CONFIGS
}