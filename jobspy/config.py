# ========================================
# EXPANDED IT JOB SCRAPER CONFIGURATION
# Split into granular workflow chunks
# ========================================

# --- Base parameters ---
DEFAULT_SITES = ["linkedin", "indeed", "glassdoor", "google", "bayt", "naukri", "bdjobs"]
DEFAULT_RESULTS = 20  # Optimized for speed vs data balance
DEFAULT_HOURS = 72
DEFAULT_DELAY = 0  # No delay - sites can handle it

# --- Major Location Groups ---
US_MAJOR_CITIES = ["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", 
                   "Boston, MA", "Los Angeles, CA", "Chicago, IL", "Denver, CO",
                   "San Diego, CA", "Portland, OR", "Atlanta, GA", "Raleigh, NC"]

EUROPE_MAJOR = ["London, United Kingdom", "Berlin, Germany", "Paris, France", 
                "Amsterdam, Netherlands", "Stockholm, Sweden", "Warsaw, Poland",
                "Dublin, Ireland", "Barcelona, Spain", "Zurich, Switzerland"]

ASIA_PACIFIC = ["Bangalore, India", "Mumbai, India", "Singapore", "Tokyo, Japan",
                "Sydney, Australia", "Melbourne, Australia", "Hong Kong", "Seoul, South Korea"]

CANADA_CITIES = ["Toronto, Canada", "Vancouver, Canada", "Montreal, Canada", "Calgary, Canada"]

# ========================================
# WORKFLOW 1: SOFTWARE ENGINEERING - GENERAL
# ========================================
SE_GENERAL_US = [
    {"query_id": "software_engineer_usa", "search_term": "software engineer", "location": "United States"},
    {"query_id": "swe_usa", "search_term": "swe", "location": "United States"},
    {"query_id": "software_developer_usa", "search_term": "software developer", "location": "United States"},
    {"query_id": "application_developer_usa", "search_term": "application developer", "location": "United States"},
]

SE_GENERAL_US.extend([
    {"query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}", 
     "search_term": "software engineer", "location": city}
    for city in US_MAJOR_CITIES
])

# ========================================
# WORKFLOW 2: SOFTWARE ENGINEERING - LEVELS (ENTRY)
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
    "entry level engineer"
]

for term in entry_level_terms:
    # Nationwide
    SE_ENTRY_LEVEL.append({
        "query_id": f"{term.replace(' ', '_').replace('.', '')}_usa",
        "search_term": term,
        "location": "United States"
    })

# Entry level in major cities (top terms only - reduced to top 3 cities)
entry_top_terms = ["junior software engineer", "entry level software engineer", "new grad software engineer"]
for term in entry_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_ENTRY_LEVEL.append({
            "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": term,
            "location": city
        })

# ========================================
# WORKFLOW 3: SOFTWARE ENGINEERING - LEVELS (MID)
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
    "intermediate software engineer"
]

for term in mid_level_terms:
    # Nationwide
    SE_MID_LEVEL.append({
        "query_id": f"{term.replace(' ', '_').replace('-', '_')}_usa",
        "search_term": term,
        "location": "United States"
    })

# Mid-level in major cities (top terms - reduced to top 3 cities)
mid_top_terms = ["software engineer", "software developer", "software engineer ii"]
for term in mid_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_MID_LEVEL.append({
            "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": term,
            "location": city
        })

# ========================================
# WORKFLOW 4: SOFTWARE ENGINEERING - LEVELS (SENIOR)
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
    "senior member technical staff"
]

for term in senior_terms:
    # Nationwide
    SE_SENIOR_LEVEL.append({
        "query_id": f"{term.replace(' ', '_')}_usa",
        "search_term": term,
        "location": "United States"
    })

# Senior in major cities (top terms - reduced to top 3 cities)
senior_top_terms = ["senior software engineer", "staff software engineer", "principal software engineer"]
for term in senior_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_SENIOR_LEVEL.append({
            "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": term,
            "location": city
        })

# ========================================
# WORKFLOW 5: SOFTWARE ENGINEERING - LEAD & ARCHITECT
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
    "technical architect"
]

for term in lead_architect_terms:
    # Nationwide
    SE_LEAD_ARCHITECT.append({
        "query_id": f"{term.replace(' ', '_')}_usa",
        "search_term": term,
        "location": "United States"
    })

# Lead/Architect in top tech hubs (reduced to top 3 cities)
lead_top_terms = ["lead software engineer", "technical lead", "software architect"]
for term in lead_top_terms:
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA"]:
        SE_LEAD_ARCHITECT.append({
            "query_id": f"{term.replace(' ', '_')}_{city.split(',')[0].lower().replace(' ', '_')}",
            "search_term": term,
            "location": city
        })

# Combine for backward compatibility
SE_LEVELS = SE_ENTRY_LEVEL + SE_MID_LEVEL + SE_SENIOR_LEVEL + SE_LEAD_ARCHITECT

# ========================================
# WORKFLOW 3: SOFTWARE ENGINEERING - INTERNATIONAL
# ========================================
SE_INTERNATIONAL = []
for city in EUROPE_MAJOR + ASIA_PACIFIC + CANADA_CITIES:
    SE_INTERNATIONAL.append({
        "query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}", 
        "search_term": "software engineer", 
        "location": city
    })

# Focused EU capitals workflow
EU_CAPITALS = [
    "Vienna, Austria",
    "Brussels, Belgium",
    "Sofia, Bulgaria",
    "Zagreb, Croatia",
    "Nicosia, Cyprus",
    "Prague, Czech Republic",
    "Copenhagen, Denmark",
    "Tallinn, Estonia",
    "Helsinki, Finland",
    "Paris, France",
    "Berlin, Germany",
    "Athens, Greece",
    "Budapest, Hungary",
    "Dublin, Ireland",
    "Rome, Italy",
    "Riga, Latvia",
    "Vilnius, Lithuania",
    "Luxembourg, Luxembourg",
    "Valletta, Malta",
    "Amsterdam, Netherlands",
    "Warsaw, Poland",
    "Lisbon, Portugal",
    "Bucharest, Romania",
    "Bratislava, Slovakia",
    "Ljubljana, Slovenia",
    "Madrid, Spain",
    "Stockholm, Sweden",
]

SE_EU_CAPITALS = []
for city in EU_CAPITALS:
    SE_EU_CAPITALS.append({
        "query_id": f"software_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
        "search_term": "software engineer",
        "location": city,
    })

# ========================================
# WORKFLOW 4: FRONTEND DEVELOPMENT
# ========================================
FRONTEND_CONFIGS = [
    {"query_id": "frontend_developer", "search_term": "frontend developer", "location": "United States"},
    {"query_id": "front_end_developer", "search_term": "front end developer", "location": "United States"},
    {"query_id": "react_developer", "search_term": "react developer", "location": "United States"},
    {"query_id": "angular_developer", "search_term": "angular developer", "location": "United States"},
    {"query_id": "vue_developer", "search_term": "vue developer", "location": "United States"},
    {"query_id": "javascript_developer", "search_term": "javascript developer", "location": "United States"},
    {"query_id": "typescript_developer", "search_term": "typescript developer", "location": "United States"},
    {"query_id": "ui_developer", "search_term": "ui developer", "location": "United States"},
    {"query_id": "web_developer", "search_term": "web developer", "location": "United States"},
]

FRONTEND_CONFIGS.extend([
    {"query_id": f"frontend_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "frontend developer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 5: BACKEND DEVELOPMENT
# ========================================
BACKEND_CONFIGS = [
    {"query_id": "backend_developer", "search_term": "backend developer", "location": "United States"},
    {"query_id": "back_end_developer", "search_term": "back end developer", "location": "United States"},
    {"query_id": "java_developer", "search_term": "java developer", "location": "United States"},
    {"query_id": "python_developer", "search_term": "python developer", "location": "United States"},
    {"query_id": "nodejs_developer", "search_term": "node.js developer", "location": "United States"},
    {"query_id": "dotnet_developer", "search_term": ".net developer", "location": "United States"},
    {"query_id": "csharp_developer", "search_term": "c# developer", "location": "United States"},
    {"query_id": "golang_developer", "search_term": "golang developer", "location": "United States"},
    {"query_id": "ruby_developer", "search_term": "ruby developer", "location": "United States"},
    {"query_id": "php_developer", "search_term": "php developer", "location": "United States"},
    {"query_id": "scala_developer", "search_term": "scala developer", "location": "United States"},
]

BACKEND_CONFIGS.extend([
    {"query_id": f"backend_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "backend developer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 6: FULLSTACK DEVELOPMENT
# ========================================
FULLSTACK_CONFIGS = [
    {"query_id": "fullstack_developer_usa", "search_term": "full stack developer", "location": "United States"},
    {"query_id": "full_stack_engineer", "search_term": "full stack engineer", "location": "United States"},
    {"query_id": "fullstack_engineer", "search_term": "fullstack engineer", "location": "United States"},
    {"query_id": "mern_developer", "search_term": "mern stack developer", "location": "United States"},
    {"query_id": "mean_developer", "search_term": "mean stack developer", "location": "United States"},
]

# Add major cities for fullstack
FULLSTACK_CONFIGS.extend([
    {"query_id": f"fullstack_{city.split(',')[0].lower().replace(' ', '_')}", 
     "search_term": "full stack developer", "location": city}
    for city in US_MAJOR_CITIES[:6]  # Top 6 cities
])

FULLSTACK_CONFIGS.extend([
    {"query_id": f"fullstack_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "full stack developer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 7: DATA SCIENCE
# ========================================
DATA_SCIENCE_CONFIGS = [
    {"query_id": "data_scientist_usa", "search_term": "data scientist", "location": "United States"},
    {"query_id": "junior_data_scientist", "search_term": "junior data scientist", "location": "United States"},
    {"query_id": "senior_data_scientist", "search_term": "senior data scientist", "location": "United States"},
    {"query_id": "lead_data_scientist", "search_term": "lead data scientist", "location": "United States"},
    {"query_id": "research_scientist", "search_term": "research scientist", "location": "United States"},
    {"query_id": "applied_scientist", "search_term": "applied scientist", "location": "United States"},
]

# Add major tech hubs for data science
DATA_SCIENCE_CONFIGS.extend([
    {"query_id": f"data_scientist_{city.split(',')[0].lower().replace(' ', '_')}", 
     "search_term": "data scientist", "location": city}
    for city in ["San Francisco, CA", "New York, NY", "Seattle, WA", "Boston, MA", "Austin, TX"]
])

DATA_SCIENCE_CONFIGS.extend([
    {"query_id": f"data_scientist_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "data scientist", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 8: DATA ENGINEERING
# ========================================
DATA_ENGINEERING_CONFIGS = [
    {"query_id": "data_engineer_usa", "search_term": "data engineer", "location": "United States"},
    {"query_id": "senior_data_engineer", "search_term": "senior data engineer", "location": "United States"},
    {"query_id": "etl_developer", "search_term": "etl developer", "location": "United States"},
    {"query_id": "big_data_engineer", "search_term": "big data engineer", "location": "United States"},
    {"query_id": "data_pipeline_engineer", "search_term": "data pipeline engineer", "location": "United States"},
    {"query_id": "analytics_engineer", "search_term": "analytics engineer", "location": "United States"},
    {"query_id": "spark_developer", "search_term": "spark developer", "location": "United States"},
]

DATA_ENGINEERING_CONFIGS.extend([
    {"query_id": f"data_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "data engineer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 9: DATA ANALYTICS
# ========================================
DATA_ANALYTICS_CONFIGS = [
    {"query_id": "data_analyst", "search_term": "data analyst", "location": "United States"},
    {"query_id": "business_analyst", "search_term": "business analyst", "location": "United States"},
    {"query_id": "business_intelligence_analyst", "search_term": "business intelligence analyst", "location": "United States"},
    {"query_id": "bi_developer", "search_term": "bi developer", "location": "United States"},
    {"query_id": "sql_developer", "search_term": "sql developer", "location": "United States"},
    {"query_id": "tableau_developer", "search_term": "tableau developer", "location": "United States"},
    {"query_id": "power_bi_developer", "search_term": "power bi developer", "location": "United States"},
]

# ========================================
# WORKFLOW 10: MACHINE LEARNING & AI
# ========================================
ML_AI_CONFIGS = [
    {"query_id": "machine_learning_engineer", "search_term": "machine learning engineer", "location": "United States"},
    {"query_id": "ml_engineer", "search_term": "ml engineer", "location": "United States"},
    {"query_id": "ai_engineer", "search_term": "ai engineer", "location": "United States"},
    {"query_id": "deep_learning_engineer", "search_term": "deep learning engineer", "location": "United States"},
    {"query_id": "nlp_engineer", "search_term": "nlp engineer", "location": "United States"},
    {"query_id": "computer_vision_engineer", "search_term": "computer vision engineer", "location": "United States"},
    {"query_id": "mlops_engineer", "search_term": "mlops engineer", "location": "United States"},
    {"query_id": "ai_research_scientist", "search_term": "ai research scientist", "location": "United States"},
    {"query_id": "prompt_engineer", "search_term": "prompt engineer", "location": "United States"},
    {"query_id": "llm_engineer", "search_term": "llm engineer", "location": "United States"},
]

# ========================================
# WORKFLOW 11: DEVOPS
# ========================================
DEVOPS_CONFIGS = [
    {"query_id": "devops_engineer", "search_term": "devops engineer", "location": "United States"},
    {"query_id": "site_reliability_engineer", "search_term": "site reliability engineer", "location": "United States"},
    {"query_id": "sre", "search_term": "sre", "location": "United States"},
    {"query_id": "platform_engineer", "search_term": "platform engineer", "location": "United States"},
    {"query_id": "infrastructure_engineer", "search_term": "infrastructure engineer", "location": "United States"},
    {"query_id": "release_engineer", "search_term": "release engineer", "location": "United States"},
    {"query_id": "build_engineer", "search_term": "build engineer", "location": "United States"},
]

DEVOPS_CONFIGS.extend([
    {"query_id": f"devops_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "devops engineer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 12: CLOUD ENGINEERING
# ========================================
CLOUD_CONFIGS = [
    {"query_id": "cloud_engineer", "search_term": "cloud engineer", "location": "United States"},
    {"query_id": "aws_engineer", "search_term": "aws engineer", "location": "United States", "results_wanted": 80},
    {"query_id": "azure_engineer", "search_term": "azure engineer", "location": "United States", "results_wanted": 80},
    {"query_id": "gcp_engineer", "search_term": "gcp engineer", "location": "United States"},
    {"query_id": "cloud_architect", "search_term": "cloud architect", "location": "United States"},
    {"query_id": "aws_architect", "search_term": "aws architect", "location": "United States"},
    {"query_id": "azure_architect", "search_term": "azure architect", "location": "United States"},
    {"query_id": "cloud_security_engineer", "search_term": "cloud security engineer", "location": "United States"},
]

# ========================================
# WORKFLOW 13: MOBILE DEVELOPMENT
# ========================================
MOBILE_CONFIGS = [
    {"query_id": "mobile_developer", "search_term": "mobile developer", "location": "United States"},
    {"query_id": "ios_developer", "search_term": "ios developer", "location": "United States", "results_wanted": 80},
    {"query_id": "android_developer", "search_term": "android developer", "location": "United States", "results_wanted": 80},
    {"query_id": "react_native_developer", "search_term": "react native developer", "location": "United States"},
    {"query_id": "flutter_developer", "search_term": "flutter developer", "location": "United States"},
    {"query_id": "swift_developer", "search_term": "swift developer", "location": "United States"},
    {"query_id": "kotlin_developer", "search_term": "kotlin developer", "location": "United States"},
]

MOBILE_CONFIGS.extend([
    {"query_id": f"mobile_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "mobile developer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 14: QA & TESTING
# ========================================
QA_TESTING_CONFIGS = [
    {"query_id": "qa_engineer", "search_term": "qa engineer", "location": "United States"},
    {"query_id": "test_engineer", "search_term": "test engineer", "location": "United States"},
    {"query_id": "sdet", "search_term": "sdet", "location": "United States"},
    {"query_id": "automation_engineer", "search_term": "automation engineer", "location": "United States"},
    {"query_id": "test_automation_engineer", "search_term": "test automation engineer", "location": "United States"},
    {"query_id": "qa_analyst", "search_term": "qa analyst", "location": "United States"},
    {"query_id": "quality_assurance_engineer", "search_term": "quality assurance engineer", "location": "United States"},
    {"query_id": "performance_test_engineer", "search_term": "performance test engineer", "location": "United States"},
]

# ========================================
# WORKFLOW 15: CYBERSECURITY
# ========================================
SECURITY_CONFIGS = [
    {"query_id": "security_engineer", "search_term": "security engineer", "location": "United States", "results_wanted": 80},
    {"query_id": "cybersecurity_engineer", "search_term": "cybersecurity engineer", "location": "United States"},
    {"query_id": "information_security_analyst", "search_term": "information security analyst", "location": "United States"},
    {"query_id": "security_analyst", "search_term": "security analyst", "location": "United States"},
    {"query_id": "penetration_tester", "search_term": "penetration tester", "location": "United States"},
    {"query_id": "ethical_hacker", "search_term": "ethical hacker", "location": "United States"},
    {"query_id": "security_architect", "search_term": "security architect", "location": "United States"},
    {"query_id": "incident_response_analyst", "search_term": "incident response analyst", "location": "United States"},
    {"query_id": "threat_intelligence_analyst", "search_term": "threat intelligence analyst", "location": "United States"},
]

SECURITY_CONFIGS.extend([
    {"query_id": f"security_engineer_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "security engineer", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 16: DATABASE ADMINISTRATION
# ========================================
DATABASE_CONFIGS = [
    {"query_id": "database_administrator", "search_term": "database administrator", "location": "United States"},
    {"query_id": "dba", "search_term": "dba", "location": "United States"},
    {"query_id": "database_engineer", "search_term": "database engineer", "location": "United States"},
    {"query_id": "sql_server_dba", "search_term": "sql server dba", "location": "United States"},
    {"query_id": "oracle_dba", "search_term": "oracle dba", "location": "United States"},
    {"query_id": "postgresql_dba", "search_term": "postgresql dba", "location": "United States"},
    {"query_id": "mongodb_developer", "search_term": "mongodb developer", "location": "United States"},
]

# ========================================
# WORKFLOW 17: PRODUCT & PROJECT MANAGEMENT (TECH)
# ========================================
PRODUCT_PROJECT_CONFIGS = [
    {"query_id": "technical_product_manager", "search_term": "technical product manager", "location": "United States"},
    {"query_id": "product_manager_tech", "search_term": "product manager", "location": "United States"},
    {"query_id": "technical_project_manager", "search_term": "technical project manager", "location": "United States"},
    {"query_id": "it_project_manager", "search_term": "it project manager", "location": "United States"},
    {"query_id": "scrum_master", "search_term": "scrum master", "location": "United States"},
    {"query_id": "agile_coach", "search_term": "agile coach", "location": "United States"},
    {"query_id": "program_manager_tech", "search_term": "program manager technical", "location": "United States"},
]

PRODUCT_PROJECT_CONFIGS.extend([
    {"query_id": f"product_manager_{city.split(',')[0].lower().replace(' ', '_')}",
     "search_term": "product manager", "location": city}
    for city in EU_CAPITALS
])

# ========================================
# WORKFLOW 18: UI/UX & DESIGN (TECH)
# ========================================
DESIGN_CONFIGS = [
    {"query_id": "ui_ux_designer", "search_term": "ui ux designer", "location": "United States"},
    {"query_id": "product_designer", "search_term": "product designer", "location": "United States"},
    {"query_id": "ux_designer", "search_term": "ux designer", "location": "United States"},
    {"query_id": "ui_designer", "search_term": "ui designer", "location": "United States"},
    {"query_id": "ux_researcher", "search_term": "ux researcher", "location": "United States"},
    {"query_id": "interaction_designer", "search_term": "interaction designer", "location": "United States"},
]

# ========================================
# WORKFLOW 19: SYSTEMS & NETWORK
# ========================================
SYSTEMS_NETWORK_CONFIGS = [
    {"query_id": "systems_engineer", "search_term": "systems engineer", "location": "United States"},
    {"query_id": "systems_administrator", "search_term": "systems administrator", "location": "United States"},
    {"query_id": "network_engineer", "search_term": "network engineer", "location": "United States"},
    {"query_id": "network_administrator", "search_term": "network administrator", "location": "United States"},
    {"query_id": "linux_administrator", "search_term": "linux administrator", "location": "United States"},
    {"query_id": "windows_administrator", "search_term": "windows administrator", "location": "United States"},
    {"query_id": "it_support_engineer", "search_term": "it support engineer", "location": "United States"},
]

# ========================================
# WORKFLOW 20: EMERGING TECH
# ========================================
EMERGING_TECH_CONFIGS = [
    {"query_id": "blockchain_developer", "search_term": "blockchain developer", "location": "United States"},
    {"query_id": "web3_developer", "search_term": "web3 developer", "location": "United States"},
    {"query_id": "smart_contract_developer", "search_term": "smart contract developer", "location": "United States"},
    {"query_id": "solidity_developer", "search_term": "solidity developer", "location": "United States"},
    {"query_id": "iot_engineer", "search_term": "iot engineer", "location": "United States"},
    {"query_id": "embedded_software_engineer", "search_term": "embedded software engineer", "location": "United States"},
    {"query_id": "robotics_engineer", "search_term": "robotics engineer", "location": "United States"},
    {"query_id": "quantum_computing_engineer", "search_term": "quantum computing engineer", "location": "United States"},
]

# ========================================
# WORKFLOW 21: REMOTE OPPORTUNITIES
# ========================================
REMOTE_CONFIGS = [
    {"query_id": "software_engineer_remote", "search_term": "software engineer", "location": "Remote"},
    {"query_id": "fullstack_remote", "search_term": "full stack developer", "location": "Remote"},
    {"query_id": "frontend_remote", "search_term": "frontend developer", "location": "Remote"},
    {"query_id": "backend_remote", "search_term": "backend developer", "location": "Remote"},
    {"query_id": "data_scientist_remote", "search_term": "data scientist", "location": "Remote"},
    {"query_id": "data_engineer_remote", "search_term": "data engineer", "location": "Remote"},
    {"query_id": "devops_remote", "search_term": "devops engineer", "location": "Remote"},
    {"query_id": "cloud_engineer_remote", "search_term": "cloud engineer", "location": "Remote"},
]

# ========================================
# WORKFLOW 22: INTERNSHIPS & ENTRY LEVEL
# ========================================
INTERNSHIP_ENTRY_CONFIGS = [
    {"query_id": "software_engineer_intern", "search_term": "software engineer intern", "location": "United States", "hours_old": 168},
    {"query_id": "software_engineering_internship", "search_term": "software engineering internship", "location": "United States", "hours_old": 168},
    {"query_id": "data_science_intern", "search_term": "data science intern", "location": "United States", "hours_old": 168},
    {"query_id": "frontend_intern", "search_term": "frontend developer intern", "location": "United States", "hours_old": 168},
    {"query_id": "new_grad_software_engineer", "search_term": "new grad software engineer", "location": "United States"},
    {"query_id": "graduate_software_engineer", "search_term": "graduate software engineer", "location": "United States"},
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
    SE_GENERAL_US, SE_ENTRY_LEVEL, SE_MID_LEVEL, SE_SENIOR_LEVEL, SE_LEAD_ARCHITECT, SE_INTERNATIONAL, SE_EU_CAPITALS,
    FRONTEND_CONFIGS, BACKEND_CONFIGS, FULLSTACK_CONFIGS,
    DATA_SCIENCE_CONFIGS, DATA_ENGINEERING_CONFIGS, DATA_ANALYTICS_CONFIGS,
    ML_AI_CONFIGS, DEVOPS_CONFIGS, CLOUD_CONFIGS,
    MOBILE_CONFIGS, QA_TESTING_CONFIGS, SECURITY_CONFIGS,
    DATABASE_CONFIGS, PRODUCT_PROJECT_CONFIGS, DESIGN_CONFIGS,
    SYSTEMS_NETWORK_CONFIGS, EMERGING_TECH_CONFIGS, REMOTE_CONFIGS,
    INTERNSHIP_ENTRY_CONFIGS
]

for config_group in ALL_WORKFLOW_CONFIGS:
    apply_defaults(config_group)

# ========================================
# WORKFLOW MAPPING
# ========================================
CONFIG_GROUPS = {
    # Software Engineering (6 workflows - split by level)
    "se_general_us": SE_GENERAL_US,
    "se_entry": SE_ENTRY_LEVEL,
    "se_mid": SE_MID_LEVEL,
    "se_senior": SE_SENIOR_LEVEL,
    "se_lead_architect": SE_LEAD_ARCHITECT,
    "se_international": SE_INTERNATIONAL,
    "se_eu_capitals": SE_EU_CAPITALS,
    
    # Web Development (3 workflows)
    "frontend": FRONTEND_CONFIGS,
    "backend": BACKEND_CONFIGS,
    "fullstack": FULLSTACK_CONFIGS,
    
    # Data (3 workflows)
    "data_science": DATA_SCIENCE_CONFIGS,
    "data_engineering": DATA_ENGINEERING_CONFIGS,
    "data_analytics": DATA_ANALYTICS_CONFIGS,
    
    # ML & AI (1 workflow)
    "ml_ai": ML_AI_CONFIGS,
    
    # Infrastructure (2 workflows)
    "devops": DEVOPS_CONFIGS,
    "cloud": CLOUD_CONFIGS,
    
    # Mobile (1 workflow)
    "mobile": MOBILE_CONFIGS,
    
    # Quality & Security (2 workflows)
    "qa_testing": QA_TESTING_CONFIGS,
    "security": SECURITY_CONFIGS,
    
    # Databases (1 workflow)
    "database": DATABASE_CONFIGS,
    
    # Management & Design (2 workflows)
    "product_project": PRODUCT_PROJECT_CONFIGS,
    "design": DESIGN_CONFIGS,
    
    # Systems & Network (1 workflow)
    "systems_network": SYSTEMS_NETWORK_CONFIGS,
    
    # Emerging Tech (1 workflow)
    "emerging_tech": EMERGING_TECH_CONFIGS,
    
    # Special Categories (2 workflows)
    "remote": REMOTE_CONFIGS,
    "internship_entry": INTERNSHIP_ENTRY_CONFIGS,
    
    # Combined views
    "all_data": DATA_SCIENCE_CONFIGS + DATA_ENGINEERING_CONFIGS + DATA_ANALYTICS_CONFIGS,
    "all_web": FRONTEND_CONFIGS + BACKEND_CONFIGS + FULLSTACK_CONFIGS,
    "all_se": SE_GENERAL_US + SE_ENTRY_LEVEL + SE_MID_LEVEL + SE_SENIOR_LEVEL + SE_LEAD_ARCHITECT + SE_INTERNATIONAL + SE_EU_CAPITALS,
    "all_se_levels": SE_ENTRY_LEVEL + SE_MID_LEVEL + SE_SENIOR_LEVEL + SE_LEAD_ARCHITECT,
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