SEARCH_CONFIGS = [
    # Software Engineering roles - Test with fewer sites first
    {
        "query_id": "software_engineer_usa",
        "site_name": ["linkedin", "indeed"],  # Removed zip_recruiter and google due to geo-blocking
        "search_term": "software engineer",
        "location": "United States",
        "results_wanted": 50,  # Reduced for testing
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_sf",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 150,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_ny",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "software engineer",
        "location": "New York, NY",
        "results_wanted": 150,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_austin",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "software engineer",
        "location": "Austin, TX",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_seattle",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "software engineer",
        "location": "Seattle, WA",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },

    # Python/Data Science roles
    {
        "query_id": "python_developer_remote",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "python developer",
        "location": "Remote",
        "results_wanted": 150,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "data_engineer_usa",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "data engineer",
        "location": "United States",
        "results_wanted": 150,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "data_scientist_usa",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "data scientist",
        "location": "United States",
        "results_wanted": 150,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "machine_learning_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "machine learning engineer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },

    # Frontend/Backend roles
    {
        "query_id": "frontend_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "frontend developer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "backend_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "backend developer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "fullstack_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "full stack developer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },

    # DevOps/Cloud roles
    {
        "query_id": "devops_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "devops engineer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "cloud_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "cloud engineer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "aws_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "aws engineer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },

    # Mobile Development
    {
        "query_id": "ios_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "ios developer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "android_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "android developer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },

    # Specialized roles
    {
        "query_id": "security_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "security engineer",
        "location": "United States",
        "results_wanted": 80,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "blockchain_developer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "blockchain developer",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 72,
        "delay": 3
    },

    # Entry level roles
    {
        "query_id": "junior_software_engineer",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "junior software engineer",
        "location": "United States",
        "results_wanted": 100,
        "hours_old": 72,
        "delay": 3
    },
    {
        "query_id": "software_engineer_intern",
        "site_name": ["linkedin", "indeed", "zip_recruiter"],
        "search_term": "software engineer intern",
        "location": "United States",
        "results_wanted": 50,
        "hours_old": 168,  # 1 week for internships
        "delay": 2
    }
]