# ========================================
# EXPANDED IT JOB SCRAPER CONFIGURATION
# Split into granular workflow chunks
# ========================================

# --- Base parameters ---
# Use only the most stable, broadly applicable providers by default.
# Glassdoor, Bayt, Naukri, and BDJobs can be re-enabled per-config if needed,
# but they frequently return 400/403/406 or region-specific blocks.
DEFAULT_SITES = ["linkedin", "indeed"]
DEFAULT_RESULTS = 120  # Optimized for speed vs data balance
DEFAULT_HOURS = 168
DEFAULT_DELAY = 0  # No delay - sites can handle it

# --- Major Location Groups ---
US_MAJOR_CITIES = [
    "San Francisco, CA",
    "New York, NY",
    "Austin, TX",
    "Seattle, WA",
    "Boston, MA",
    "Los Angeles, CA",
    "Chicago, IL",
    "Denver, CO",
    "San Diego, CA",
    "Portland, OR",
    "Atlanta, GA",
    "Raleigh, NC",
]

EUROPE_MAJOR = [
    "London, United Kingdom",
    "Berlin, Germany",
    "Paris, France",
    "Amsterdam, Netherlands",
    "Stockholm, Sweden",
    "Warsaw, Poland",
    "Barcelona, Spain",
    "Zurich, Switzerland",
]

ASIA_PACIFIC = ["Sydney, Australia", "Melbourne, Australia"]

CANADA_CITIES = [
    "Toronto, Canada",
    "Vancouver, Canada",
    "Montreal, Canada",
    "Calgary, Canada",
]

# NOTE: Only the groups listed in CONFIG_GROUPS (near the bottom of this file)
# are actively used by main.py. Other workflow blocks below are kept for
# reference but are not included in CONFIG_GROUPS.

# ========================================
# LEGACY WORKFLOW: SOFTWARE ENGINEERING - GENERAL (not in CONFIG_GROUPS)
# ========================================
SE_GENERAL_US = [
    {
        "query_id": "software_engineer_usa",
        "search_term": "software engineer",
        "location": "United States",
    },
    {"query_id": "swe_usa", "search_term": "swe", "location": "United States"},
    {
        "query_id": "software_developer_usa",
        "search_term": "software developer",
        "location": "United States",
    },
    {
        "query_id": "application_developer_usa",
        "search_term": "application developer",
        "location": "United States",
    },
]

SE_GENERAL_US.extend(
    [
        {
            "query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "software engineer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

# ========================================
# LEGACY WORKFLOW: SOFTWARE ENGINEERING - LEVELS (ENTRY) (not in CONFIG_GROUPS)
# ========================================
SE_ENTRY_LEVEL = []

# All entry level variations
entry_level_terms = [
    "junior software engineer",
    "junior software developer",
    "jr software engineer",
    "jr software developer",
    "entry level software engineer",
    "entry level software developer",
    "associate software engineer",
    "associate software developer",
    "software engineer i",
    "software developer i",
    "software engineer 1",
    "graduate software engineer",
    "new grad software engineer",
    "early career software engineer",
    "software engineer new grad",
    "associate engineer",
    "junior engineer",
    "entry level engineer",
]

for term in entry_level_terms:
    # Nationwide
    SE_ENTRY_LEVEL.append(
        {
            "query_id": f"{term.replace(' ', '_').replace('.', '')}_usa",
            "search_term": term,
            "location": "United States",
        }
    )

# Entry level in major cities (top terms only - reduced to top 3 cities)
entry_top_terms = [
    "junior software engineer",
    "entry level software engineer",
    "new grad software engineer",
]
for term in entry_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_ENTRY_LEVEL.append(
            {
                "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
                "search_term": term,
                "location": city,
            }
        )

# ========================================
# LEGACY WORKFLOW: SOFTWARE ENGINEERING - LEVELS (MID) (not in CONFIG_GROUPS)
# ========================================
SE_MID_LEVEL = []

# Mid-level variations (no level prefix, or level II/2)
mid_level_terms = [
    "software engineer",
    "software developer",
    "software engineer ii",
    "software developer ii",
    "software engineer 2",
    "software developer 2",
    "software engineer iii",
    "software developer iii",
    "software engineer 3",
    "software developer 3",
    "mid level software engineer",
    "mid-level software engineer",
    "intermediate software engineer",
]

for term in mid_level_terms:
    # Nationwide
    SE_MID_LEVEL.append(
        {
            "query_id": f"{term.replace(' ', '_').replace('-', '_')}_usa",
            "search_term": term,
            "location": "United States",
        }
    )

# Mid-level in major cities (top terms - reduced to top 3 cities)
mid_top_terms = ["software engineer", "software developer", "software engineer ii"]
for term in mid_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_MID_LEVEL.append(
            {
                "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
                "search_term": term,
                "location": city,
            }
        )

# ========================================
# LEGACY WORKFLOW: SOFTWARE ENGINEERING - LEVELS (SENIOR) (not in CONFIG_GROUPS)
# ========================================
SE_SENIOR_LEVEL = []

# Senior level variations
senior_terms = [
    "senior software engineer",
    "senior software developer",
    "sr software engineer",
    "sr software developer",
    "senior swe",
    "staff software engineer",
    "staff software developer",
    "staff engineer",
    "principal software engineer",
    "principal software developer",
    "principal engineer",
    "senior engineer",
    "software engineer iv",
    "software developer iv",
    "software engineer 4",
    "senior member technical staff",
]

for term in senior_terms:
    # Nationwide
    SE_SENIOR_LEVEL.append(
        {
            "query_id": f"{term.replace(' ', '_')}_usa",
            "search_term": term,
            "location": "United States",
        }
    )

# Senior in major cities (top terms - reduced to top 3 cities)
senior_top_terms = [
    "senior software engineer",
    "staff software engineer",
    "principal software engineer",
]
for term in senior_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_SENIOR_LEVEL.append(
            {
                "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
                "search_term": term,
                "location": city,
            }
        )

# ========================================
# LEGACY WORKFLOW: SOFTWARE ENGINEERING - LEAD & ARCHITECT (not in CONFIG_GROUPS)
# ========================================
SE_LEAD_ARCHITECT = []

# Lead and architect variations
lead_architect_terms = [
    "lead software engineer",
    "lead engineer",
    "engineering lead",
    "technical lead",
    "tech lead",
    "lead developer",
    "software architect",
    "solutions architect",
    "enterprise architect",
    "principal architect",
    "staff architect",
    "senior architect",
    "cloud solutions architect",
    "application architect",
    "systems architect",
    "lead software developer",
    "engineering manager",  # Often IC track
    "technical architect",
]

for term in lead_architect_terms:
    # Nationwide
    SE_LEAD_ARCHITECT.append(
        {
            "query_id": f"{term.replace(' ', '_')}_usa",
            "search_term": term,
            "location": "United States",
        }
    )

# Lead/Architect in top tech hubs (reduced to top 3 cities)
lead_top_terms = ["lead software engineer", "technical lead", "software architect"]
for term in lead_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_LEAD_ARCHITECT.append(
            {
                "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
                "search_term": term,
                "location": city,
            }
        )

# Combine for backward compatibility
SE_LEVELS = SE_ENTRY_LEVEL + SE_MID_LEVEL + SE_SENIOR_LEVEL + SE_LEAD_ARCHITECT

SE_INTERNATIONAL = []
for city in EUROPE_MAJOR + ASIA_PACIFIC + CANADA_CITIES:
    SE_INTERNATIONAL.append(
        {
            "query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "software engineer",
            "location": city,
        }
    )

EU_CAPITALS = [
    "Paris, France",
    "Berlin, Germany",
    "Rome, Italy",
    "Amsterdam, Netherlands",
    "Warsaw, Poland",
    "Lisbon, Portugal",
    "Bratislava, Slovakia",
    "Madrid, Spain",
    "Stockholm, Sweden",
]

SE_EU_CAPITALS = []
for city in EU_CAPITALS:
    SE_EU_CAPITALS.append(
        {
            "query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "software engineer",
            "location": city,
        }
    )

# ========================================
# WORKFLOW 1: FRONTEND DEVELOPMENT
# ========================================
FRONTEND_CONFIGS = [
    {
        "query_id": "frontend_developer",
        "search_term": "frontend developer",
        "location": "United States",
    },
    {
        "query_id": "front_end_developer",
        "search_term": "front end developer",
        "location": "United States",
    },
    {
        "query_id": "react_developer",
        "search_term": "react developer",
        "location": "United States",
    },
    {
        "query_id": "angular_developer",
        "search_term": "angular developer",
        "location": "United States",
    },
    {
        "query_id": "vue_developer",
        "search_term": "vue developer",
        "location": "United States",
    },
    {
        "query_id": "javascript_developer",
        "search_term": "javascript developer",
        "location": "United States",
    },
    {
        "query_id": "typescript_developer",
        "search_term": "typescript developer",
        "location": "United States",
    },
    {
        "query_id": "ui_developer",
        "search_term": "ui developer",
        "location": "United States",
    },
    {
        "query_id": "web_developer",
        "search_term": "web developer",
        "location": "United States",
    },
]

FRONTEND_CONFIGS.extend(
    [
        {
            "query_id": f"frontend_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "frontend developer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

FRONTEND_CONFIGS.extend(
    [
        {
            "query_id": f"frontend_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "frontend developer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

FRONTEND_CONFIGS.extend(
    [
        {
            "query_id": f"frontend_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "frontend developer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

FRONTEND_CONFIGS.append(
    {
        "query_id": "frontend_remote",
        "search_term": "frontend developer",
        "location": "Remote",
    }
)

# ========================================
# WORKFLOW 2: BACKEND DEVELOPMENT
# ========================================
BACKEND_CONFIGS = [
    {
        "query_id": "backend_developer",
        "search_term": "backend developer",
        "location": "United States",
    },
    {
        "query_id": "back_end_developer",
        "search_term": "back end developer",
        "location": "United States",
    },
    {
        "query_id": "java_developer",
        "search_term": "java developer",
        "location": "United States",
    },
    {
        "query_id": "python_developer",
        "search_term": "python developer",
        "location": "United States",
    },
    {
        "query_id": "nodejs_developer",
        "search_term": "node.js developer",
        "location": "United States",
    },
    {
        "query_id": "dotnet_developer",
        "search_term": ".net developer",
        "location": "United States",
    },
    {
        "query_id": "csharp_developer",
        "search_term": "c# developer",
        "location": "United States",
    },
    {
        "query_id": "golang_developer",
        "search_term": "golang developer",
        "location": "United States",
    },
    {
        "query_id": "ruby_developer",
        "search_term": "ruby developer",
        "location": "United States",
    },
    {
        "query_id": "php_developer",
        "search_term": "php developer",
        "location": "United States",
    },
    {
        "query_id": "scala_developer",
        "search_term": "scala developer",
        "location": "United States",
    },
]

BACKEND_CONFIGS.extend(
    [
        {
            "query_id": f"backend_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "backend developer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

BACKEND_CONFIGS.extend(
    [
        {
            "query_id": f"backend_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "backend developer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

BACKEND_CONFIGS.extend(
    [
        {
            "query_id": f"backend_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "backend developer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

BACKEND_CONFIGS.append(
    {
        "query_id": "backend_remote",
        "search_term": "backend developer",
        "location": "Remote",
    }
)

# ========================================
# WORKFLOW 3: FULLSTACK DEVELOPMENT
# ========================================
FULLSTACK_CONFIGS = [
    {
        "query_id": "fullstack_developer_usa",
        "search_term": "full stack developer",
        "location": "United States",
    },
    {
        "query_id": "full_stack_engineer",
        "search_term": "full stack engineer",
        "location": "United States",
    },
    {
        "query_id": "fullstack_engineer",
        "search_term": "fullstack engineer",
        "location": "United States",
    },
    {
        "query_id": "mern_developer",
        "search_term": "mern stack developer",
        "location": "United States",
    },
    {
        "query_id": "mean_developer",
        "search_term": "mean stack developer",
        "location": "United States",
    },
]

# Add major cities for fullstack
FULLSTACK_CONFIGS.extend(
    [
        {
            "query_id": f"fullstack_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "full stack developer",
            "location": city,
        }
        for city in US_MAJOR_CITIES[:6]  # Top 6 cities
    ]
)

FULLSTACK_CONFIGS.extend(
    [
        {
            "query_id": f"fullstack_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "full stack developer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

FULLSTACK_CONFIGS.extend(
    [
        {
            "query_id": f"fullstack_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "full stack developer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

FULLSTACK_CONFIGS.extend(
    [
        {
            "query_id": f"fullstack_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "full stack developer",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

FULLSTACK_CONFIGS.append(
    {
        "query_id": "fullstack_remote",
        "search_term": "full stack developer",
        "location": "Remote",
    }
)

# ========================================
# WORKFLOW 4: DATA SCIENCE
# ========================================
DATA_SCIENCE_CONFIGS = [
    {
        "query_id": "data_scientist_usa",
        "search_term": "data scientist",
        "location": "United States",
    },
    {
        "query_id": "junior_data_scientist",
        "search_term": "junior data scientist",
        "location": "United States",
    },
    {
        "query_id": "senior_data_scientist",
        "search_term": "senior data scientist",
        "location": "United States",
    },
    {
        "query_id": "lead_data_scientist",
        "search_term": "lead data scientist",
        "location": "United States",
    },
    {
        "query_id": "research_scientist",
        "search_term": "research scientist",
        "location": "United States",
    },
    {
        "query_id": "applied_scientist",
        "search_term": "applied scientist",
        "location": "United States",
    },
]

# Add major tech hubs for data science
DATA_SCIENCE_CONFIGS.extend(
    [
        {
            "query_id": f"data_scientist_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data scientist",
            "location": city,
        }
        for city in [
            "San Francisco, CA",
            "New York, NY",
            "Seattle, WA",
            "Boston, MA",
            "Austin, TX",
        ]
    ]
)

DATA_SCIENCE_CONFIGS.extend(
    [
        {
            "query_id": f"data_scientist_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data scientist",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

DATA_SCIENCE_CONFIGS.extend(
    [
        {
            "query_id": f"data_scientist_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data scientist",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

DATA_SCIENCE_CONFIGS.extend(
    [
        {
            "query_id": f"data_scientist_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data scientist",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

DATA_SCIENCE_CONFIGS.append(
    {
        "query_id": "data_scientist_remote",
        "search_term": "data scientist",
        "location": "Remote",
    }
)

# ========================================
# WORKFLOW 5: DATA ENGINEERING
# ========================================
DATA_ENGINEERING_CONFIGS = [
    {
        "query_id": "data_engineer_usa",
        "search_term": "data engineer",
        "location": "United States",
    },
    {
        "query_id": "senior_data_engineer",
        "search_term": "senior data engineer",
        "location": "United States",
    },
    {
        "query_id": "etl_developer",
        "search_term": "etl developer",
        "location": "United States",
    },
    {
        "query_id": "big_data_engineer",
        "search_term": "big data engineer",
        "location": "United States",
    },
    {
        "query_id": "data_pipeline_engineer",
        "search_term": "data pipeline engineer",
        "location": "United States",
    },
    {
        "query_id": "analytics_engineer",
        "search_term": "analytics engineer",
        "location": "United States",
    },
    {
        "query_id": "spark_developer",
        "search_term": "spark developer",
        "location": "United States",
    },
]

DATA_ENGINEERING_CONFIGS.extend(
    [
        {
            "query_id": f"data_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data engineer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

DATA_ENGINEERING_CONFIGS.extend(
    [
        {
            "query_id": f"data_engineer_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data engineer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

DATA_ENGINEERING_CONFIGS.extend(
    [
        {
            "query_id": f"data_engineer_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data engineer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

DATA_ENGINEERING_CONFIGS.extend(
    [
        {
            "query_id": f"data_engineer_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "data engineer",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

DATA_ENGINEERING_CONFIGS.append(
    {
        "query_id": "data_engineer_remote",
        "search_term": "data engineer",
        "location": "Remote",
    }
)

# ========================================
# LEGACY WORKFLOW: MACHINE LEARNING & AI (not in CONFIG_GROUPS)
# ========================================
ML_AI_CONFIGS = [
    {
        "query_id": "machine_learning_engineer",
        "search_term": "machine learning engineer",
        "location": "United States",
    },
    {
        "query_id": "ml_engineer",
        "search_term": "ml engineer",
        "location": "United States",
    },
    {
        "query_id": "ai_engineer",
        "search_term": "ai engineer",
        "location": "United States",
    },
    {
        "query_id": "deep_learning_engineer",
        "search_term": "deep learning engineer",
        "location": "United States",
    },
    {
        "query_id": "nlp_engineer",
        "search_term": "nlp engineer",
        "location": "United States",
    },
    {
        "query_id": "computer_vision_engineer",
        "search_term": "computer vision engineer",
        "location": "United States",
    },
    {
        "query_id": "mlops_engineer",
        "search_term": "mlops engineer",
        "location": "United States",
    },
    {
        "query_id": "ai_research_scientist",
        "search_term": "ai research scientist",
        "location": "United States",
    },
    {
        "query_id": "prompt_engineer",
        "search_term": "prompt engineer",
        "location": "United States",
    },
    {
        "query_id": "llm_engineer",
        "search_term": "llm engineer",
        "location": "United States",
    },
]

# ========================================
# WORKFLOW 6: DEVOPS
# ========================================
DEVOPS_CONFIGS = [
    {
        "query_id": "devops_engineer",
        "search_term": "devops engineer",
        "location": "United States",
    },
    {
        "query_id": "site_reliability_engineer",
        "search_term": "site reliability engineer",
        "location": "United States",
    },
    {"query_id": "sre", "search_term": "sre", "location": "United States"},
    {
        "query_id": "platform_engineer",
        "search_term": "platform engineer",
        "location": "United States",
    },
    {
        "query_id": "infrastructure_engineer",
        "search_term": "infrastructure engineer",
        "location": "United States",
    },
    {
        "query_id": "release_engineer",
        "search_term": "release engineer",
        "location": "United States",
    },
    {
        "query_id": "build_engineer",
        "search_term": "build engineer",
        "location": "United States",
    },
]

DEVOPS_CONFIGS.extend(
    [
        {
            "query_id": f"devops_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "devops engineer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

DEVOPS_CONFIGS.extend(
    [
        {
            "query_id": f"devops_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "devops engineer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

DEVOPS_CONFIGS.extend(
    [
        {
            "query_id": f"devops_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "devops engineer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

DEVOPS_CONFIGS.extend(
    [
        {
            "query_id": f"devops_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "devops engineer",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

DEVOPS_CONFIGS.append(
    {
        "query_id": "devops_remote",
        "search_term": "devops engineer",
        "location": "Remote",
    }
)

# ========================================
# LEGACY WORKFLOW: CLOUD ENGINEERING (not in CONFIG_GROUPS)
# ========================================
CLOUD_CONFIGS = [
    {
        "query_id": "cloud_engineer",
        "search_term": "cloud engineer",
        "location": "United States",
    },
    {
        "query_id": "aws_engineer",
        "search_term": "aws engineer",
        "location": "United States",
        "results_wanted": 120,
    },
    {
        "query_id": "azure_engineer",
        "search_term": "azure engineer",
        "location": "United States",
        "results_wanted": 120,
    },
    {
        "query_id": "gcp_engineer",
        "search_term": "gcp engineer",
        "location": "United States",
    },
    {
        "query_id": "cloud_architect",
        "search_term": "cloud architect",
        "location": "United States",
    },
    {
        "query_id": "aws_architect",
        "search_term": "aws architect",
        "location": "United States",
    },
    {
        "query_id": "azure_architect",
        "search_term": "azure architect",
        "location": "United States",
    },
    {
        "query_id": "cloud_security_engineer",
        "search_term": "cloud security engineer",
        "location": "United States",
    },
]

# ========================================
# WORKFLOW 7: MOBILE DEVELOPMENT
# ========================================
MOBILE_CONFIGS = [
    {
        "query_id": "mobile_developer",
        "search_term": "mobile developer",
        "location": "United States",
    },
    {
        "query_id": "ios_developer",
        "search_term": "ios developer",
        "location": "United States",
        "results_wanted": 120,
    },
    {
        "query_id": "android_developer",
        "search_term": "android developer",
        "location": "United States",
        "results_wanted": 120,
    },
    {
        "query_id": "react_native_developer",
        "search_term": "react native developer",
        "location": "United States",
    },
    {
        "query_id": "flutter_developer",
        "search_term": "flutter developer",
        "location": "United States",
    },
    {
        "query_id": "swift_developer",
        "search_term": "swift developer",
        "location": "United States",
    },
    {
        "query_id": "kotlin_developer",
        "search_term": "kotlin developer",
        "location": "United States",
    },
]

MOBILE_CONFIGS.extend(
    [
        {
            "query_id": f"mobile_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "mobile developer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

MOBILE_CONFIGS.extend(
    [
        {
            "query_id": f"mobile_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "mobile developer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

MOBILE_CONFIGS.extend(
    [
        {
            "query_id": f"mobile_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "mobile developer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

MOBILE_CONFIGS.extend(
    [
        {
            "query_id": f"mobile_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "mobile developer",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

MOBILE_CONFIGS.append(
    {
        "query_id": "mobile_remote",
        "search_term": "mobile developer",
        "location": "Remote",
    }
)


# ========================================
# WORKFLOW 8: CYBERSECURITY
# ========================================
SECURITY_CONFIGS = [
    {
        "query_id": "security_engineer",
        "search_term": "security engineer",
        "location": "United States",
        "results_wanted": 120,
    },
    {
        "query_id": "cybersecurity_engineer",
        "search_term": "cybersecurity engineer",
        "location": "United States",
    },
    {
        "query_id": "information_security_analyst",
        "search_term": "information security analyst",
        "location": "United States",
    },
    {
        "query_id": "security_analyst",
        "search_term": "security analyst",
        "location": "United States",
    },
    {
        "query_id": "penetration_tester",
        "search_term": "penetration tester",
        "location": "United States",
    },
    {
        "query_id": "ethical_hacker",
        "search_term": "ethical hacker",
        "location": "United States",
    },
    {
        "query_id": "security_architect",
        "search_term": "security architect",
        "location": "United States",
    },
    {
        "query_id": "incident_response_analyst",
        "search_term": "incident response analyst",
        "location": "United States",
    },
    {
        "query_id": "threat_intelligence_analyst",
        "search_term": "threat intelligence analyst",
        "location": "United States",
    },
]

SECURITY_CONFIGS.extend(
    [
        {
            "query_id": f"security_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "security engineer",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

SECURITY_CONFIGS.extend(
    [
        {
            "query_id": f"security_engineer_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "security engineer",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

SECURITY_CONFIGS.extend(
    [
        {
            "query_id": f"security_engineer_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "security engineer",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

SECURITY_CONFIGS.extend(
    [
        {
            "query_id": f"security_engineer_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "security engineer",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)

SECURITY_CONFIGS.append(
    {
        "query_id": "security_engineer_remote",
        "search_term": "security engineer",
        "location": "Remote",
    }
)


# ========================================
# WORKFLOW 9: PRODUCT MANAGEMENT
# ========================================
PRODUCT_MANAGER_CONFIGS = [
    {
        "query_id": "product_manager",
        "search_term": "product manager",
        "location": "United States",
    },
    {
        "query_id": "technical_product_manager",
        "search_term": "technical product manager",
        "location": "United States",
    },
    {
        "query_id": "senior_product_manager",
        "search_term": "senior product manager",
        "location": "United States",
    },
    {
        "query_id": "product_owner",
        "search_term": "product owner",
        "location": "United States",
    },
    {
        "query_id": "product_manager_remote",
        "search_term": "product manager",
        "location": "Remote",
    },
]

PRODUCT_MANAGER_CONFIGS.extend(
    [
        {
            "query_id": f"product_manager_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "product manager",
            "location": city,
        }
        for city in EU_CAPITALS
    ]
)

PRODUCT_MANAGER_CONFIGS.extend(
    [
        {
            "query_id": f"product_manager_us_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "product manager",
            "location": city,
        }
        for city in US_MAJOR_CITIES
    ]
)

PRODUCT_MANAGER_CONFIGS.extend(
    [
        {
            "query_id": f"product_manager_canada_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "product manager",
            "location": city,
        }
        for city in CANADA_CITIES
    ]
)

PRODUCT_MANAGER_CONFIGS.extend(
    [
        {
            "query_id": f"product_manager_apac_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": "product manager",
            "location": city,
        }
        for city in ASIA_PACIFIC
    ]
)


# ========================================
# LEGACY WORKFLOW: REMOTE OPPORTUNITIES (not in CONFIG_GROUPS)
# ========================================
REMOTE_CONFIGS = [
    {
        "query_id": "software_engineer_remote",
        "search_term": "software engineer",
        "location": "Remote",
    },
    {
        "query_id": "fullstack_remote",
        "search_term": "full stack developer",
        "location": "Remote",
    },
    {
        "query_id": "frontend_remote",
        "search_term": "frontend developer",
        "location": "Remote",
    },
    {
        "query_id": "backend_remote",
        "search_term": "backend developer",
        "location": "Remote",
    },
    {
        "query_id": "data_scientist_remote",
        "search_term": "data scientist",
        "location": "Remote",
    },
    {
        "query_id": "data_engineer_remote",
        "search_term": "data engineer",
        "location": "Remote",
    },
    {
        "query_id": "devops_remote",
        "search_term": "devops engineer",
        "location": "Remote",
    },
    {
        "query_id": "cloud_engineer_remote",
        "search_term": "cloud engineer",
        "location": "Remote",
    },
]

# ========================================
# LEGACY WORKFLOW: INTERNSHIPS & ENTRY LEVEL (not in CONFIG_GROUPS)
# ========================================
INTERNSHIP_ENTRY_CONFIGS = [
    {
        "query_id": "software_engineer_intern",
        "search_term": "software engineer intern",
        "location": "United States",
        "hours_old": 168,
    },
    {
        "query_id": "software_engineering_internship",
        "search_term": "software engineering internship",
        "location": "United States",
        "hours_old": 168,
    },
    {
        "query_id": "data_science_intern",
        "search_term": "data science intern",
        "location": "United States",
        "hours_old": 168,
    },
    {
        "query_id": "frontend_intern",
        "search_term": "frontend developer intern",
        "location": "United States",
        "hours_old": 168,
    },
    {
        "query_id": "new_grad_software_engineer",
        "search_term": "new grad software engineer",
        "location": "United States",
    },
    {
        "query_id": "graduate_software_engineer",
        "search_term": "graduate software engineer",
        "location": "United States",
    },
]


# --- Apply defaults ---
def apply_defaults(configs):
    for cfg in configs:
        cfg.setdefault("site_name", DEFAULT_SITES)
        cfg.setdefault("results_wanted", DEFAULT_RESULTS)
        cfg.setdefault("hours_old", DEFAULT_HOURS)
        cfg.setdefault("delay", DEFAULT_DELAY)
    return configs


# Apply defaults to all configs
ALL_WORKFLOW_CONFIGS = [
    FRONTEND_CONFIGS,
    BACKEND_CONFIGS,
    FULLSTACK_CONFIGS,
    DEVOPS_CONFIGS,
    MOBILE_CONFIGS,
    DATA_ENGINEERING_CONFIGS,
    DATA_SCIENCE_CONFIGS,
    SECURITY_CONFIGS,
    PRODUCT_MANAGER_CONFIGS,
]

for config_group in ALL_WORKFLOW_CONFIGS:
    apply_defaults(config_group)

# ========================================
# WORKFLOW MAPPING
# ========================================
CONFIG_GROUPS = {
    "frontend": FRONTEND_CONFIGS,
    "backend": BACKEND_CONFIGS,
    "fullstack": FULLSTACK_CONFIGS,
    "devops": DEVOPS_CONFIGS,
    "mobile": MOBILE_CONFIGS,
    "data_engineering": DATA_ENGINEERING_CONFIGS,
    "data_science": DATA_SCIENCE_CONFIGS,
    "security": SECURITY_CONFIGS,
    "product_manager": PRODUCT_MANAGER_CONFIGS,
}


# Total count helper
def get_total_queries():
    total = sum(len(config) for config in ALL_WORKFLOW_CONFIGS)
    print(f"Total number of job queries: {total}")
    return total


# Usage examples:
# workflow_config = CONFIG_GROUPS["frontend"]
# workflow_config = CONFIG_GROUPS["ml_ai"]
# workflow_config = CONFIG_GROUPS["all_data"]
