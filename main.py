import os
import logging
import pandas as pd
from datetime import datetime
from jobspy import scrape_jobs
from jobspy.config import CONFIG_GROUPS
import psycopg2
from psycopg2.extras import execute_values
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JobDatabase:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.create_tables()

    def get_connection(self):
        return psycopg2.connect(self.connection_string)

    def create_tables(self):
        """Create the jobs table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id VARCHAR(255) PRIMARY KEY,
            site VARCHAR(50),
            job_url TEXT,
            job_url_direct TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            date_posted DATE,
            job_type VARCHAR(50),
            salary_source VARCHAR(50),
            interval VARCHAR(20),
            min_amount DECIMAL(15,2),
            max_amount DECIMAL(15,2),
            currency VARCHAR(10),
            is_remote BOOLEAN,
            job_level VARCHAR(50),
            job_function TEXT,
            listing_type VARCHAR(50),
            emails TEXT,
            description TEXT,
            company_industry TEXT,
            company_url TEXT,
            company_logo TEXT,
            company_url_direct TEXT,
            company_addresses TEXT,
            company_num_employees VARCHAR(50),
            company_revenue VARCHAR(50),
            company_description TEXT,
            skills TEXT,
            experience_range TEXT,
            company_rating DECIMAL(3,1),
            company_reviews_count INTEGER,
            vacancy_count INTEGER,
            work_from_home_type TEXT,
            seniority_level VARCHAR(20),
            role_family VARCHAR(50),
            primary_language VARCHAR(50),
            tech_tags TEXT,
            city_normalized VARCHAR(100),
            country_normalized VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_jobs_site ON jobs(site);
        CREATE INDEX IF NOT EXISTS idx_jobs_date_posted ON jobs(date_posted);
        CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
        CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);

        ALTER TABLE jobs
            ADD COLUMN IF NOT EXISTS seniority_level VARCHAR(20),
            ADD COLUMN IF NOT EXISTS role_family VARCHAR(50),
            ADD COLUMN IF NOT EXISTS primary_language VARCHAR(50),
            ADD COLUMN IF NOT EXISTS tech_tags TEXT,
            ADD COLUMN IF NOT EXISTS city_normalized VARCHAR(100),
            ADD COLUMN IF NOT EXISTS country_normalized VARCHAR(100);
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(create_table_query)
                    conn.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def job_exists(self, job_id):
        """Check if a job already exists in the database"""
        query = "SELECT id FROM jobs WHERE id = %s"
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (job_id,))
                    return cur.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking if job exists: {e}")
            return False

    def _normalize_str(self, value):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            lower = cleaned.lower()
            if lower in ("nan", "none", "null"):
                return None
            return cleaned
        return str(value)

    def _infer_seniority_level(self, title, description):
        text = f"{title or ''} {description or ''}".lower()

        if any(k in text for k in ["intern ", "internship", "trainee"]):
            return "intern"
        if any(k in text for k in ["junior", " jr ", " jr.", "entry level", "new grad", "graduate", "early career", "associate"]):
            return "entry"
        if any(k in text for k in ["lead ", "lead-", "principal", "staff", "head of", "architect"]):
            return "lead"
        if any(k in text for k in ["senior", " sr ", " sr."]):
            return "senior"
        if any(k in text for k in ["mid level", "mid-level", "intermediate", " level ii", " level 2", " level iii", " level 3"]):
            return "mid"
        if "software engineer" in text or "software developer" in text or "swe" in text:
            return "mid"
        return None

    def _infer_role_family(self, title, description):
        text = f"{title or ''} {description or ''}".lower()

        if "data scientist" in text:
            return "data_scientist"
        if any(k in text for k in ["machine learning engineer", "ml engineer", "ai engineer", "deep learning"]):
            return "ml_ai"
        if any(k in text for k in ["data engineer", "etl developer", "data pipeline engineer", "big data engineer"]):
            return "data_engineer"
        if any(k in text for k in ["data analyst", "business analyst", "bi developer", "analytics engineer"]):
            return "data_analyst"
        if any(k in text for k in ["devops", "site reliability engineer", "sre", "platform engineer", "infrastructure engineer"]):
            return "devops"
        if any(k in text for k in ["cloud engineer", "cloud architect", "aws engineer", "azure engineer", "gcp engineer"]):
            return "cloud"
        if any(k in text for k in ["security engineer", "cybersecurity", "info security", "penetration tester", "ethical hacker"]):
            return "security"
        if any(k in text for k in ["frontend", "front end", "ui developer", "react developer", "angular developer", "vue developer"]):
            return "frontend"
        if any(k in text for k in ["backend", "back end", "server-side"]):
            return "backend"
        if any(k in text for k in ["full stack", "fullstack", "mern", "mean"]):
            return "fullstack"
        if any(k in text for k in ["ios", "android", "mobile developer", "react native", "flutter", "swift developer", "kotlin developer"]):
            return "mobile"
        if any(k in text for k in ["qa engineer", "quality assurance", "test engineer", "sdet", "automation engineer"]):
            return "qa"
        if any(k in text for k in ["product manager", "product owner"]):
            return "product"
        if any(k in text for k in ["project manager", "program manager", "scrum master"]):
            return "project"
        if any(k in text for k in ["ux designer", "ui designer", "product designer", "interaction designer", "ux researcher"]):
            return "design"
        if any(k in text for k in ["software engineer", "software developer", "swe"]):
            return "software_engineer"
        return None

    def _extract_tech_tags(self, title, description):
        text = f"{title or ''} {description or ''}".lower()
        tags = set()

        patterns = {
            "python": ["python"],
            "java": [" java "],
            "javascript": ["javascript", " js "],
            "typescript": ["typescript", " ts "],
            "c++": ["c++"],
            "c#": ["c#"],
            "go": [" golang", " go "],
            "rust": ["rust"],
            "ruby": ["ruby"],
            "php": ["php"],
            "scala": ["scala"],
            "kotlin": ["kotlin"],
            "swift": ["swift"],
            "node.js": ["node.js", "nodejs"],
            "react": [" react"],
            "angular": ["angular"],
            "vue": [" vue"],
            "django": ["django"],
            "flask": ["flask"],
            "spring": ["spring boot", "spring framework"],
            "rails": ["rails", "ruby on rails"],
            "dotnet": [".net", "dotnet"],
            "aws": ["aws"],
            "azure": ["azure"],
            "gcp": ["gcp", "google cloud"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "terraform": ["terraform"],
            "ansible": ["ansible"],
            "postgres": ["postgres", "postgresql"],
            "mysql": ["mysql"],
            "mongodb": ["mongodb"],
            "redis": ["redis"],
            "kafka": ["kafka"],
            "spark": ["spark"],
        }

        for tag, needles in patterns.items():
            if any(n in text for n in needles):
                tags.add(tag)

        if not tags:
            return None, None

        language_order = [
            "python",
            "javascript",
            "typescript",
            "java",
            "c++",
            "c#",
            "go",
            "rust",
            "ruby",
            "php",
            "scala",
            "kotlin",
            "swift",
        ]

        primary_language = None
        for lang in language_order:
            if lang in tags:
                primary_language = lang
                break

        tech_tags = ",".join(sorted(tags))
        return primary_language, tech_tags

    def _normalize_location_parts(self, location):
        if not location:
            return None, None
        if isinstance(location, str):
            parts = [p.strip() for p in location.split(',') if p.strip()]
            if not parts:
                return None, None
            city = parts[0]
            country = parts[-1] if len(parts) > 1 else None
            return city, country
        return None, None

    def insert_jobs(self, jobs_df):
        """Insert new jobs into the database, skipping duplicates"""
        if jobs_df.empty:
            logger.info("No jobs to insert")
            return 0

        # Convert DataFrame to list of tuples, handling NaN values
        jobs_data = []
        for _, row in jobs_df.iterrows():
            # Convert date_posted to proper format
            date_posted = None
            raw_date = row.get('date_posted')
            if pd.notna(raw_date):
                try:
                    date_posted = pd.to_datetime(raw_date).date()
                except Exception:
                    date_posted = None

            title = row.get('title')
            raw_description = row.get('description')
            location = row.get('location')

            seniority_level = self._infer_seniority_level(title, raw_description)
            role_family = self._infer_role_family(title, raw_description)
            primary_language, tech_tags = self._extract_tech_tags(title, raw_description)
            city_norm, country_norm = self._normalize_location_parts(location)

            description_value = self._normalize_str(raw_description)

            job_tuple = (
                str(row.get('id', '')),
                str(row.get('site', '')),
                str(row.get('job_url', '')),
                str(row.get('job_url_direct', '')),
                str(row.get('title', '')),
                self._normalize_str(row.get('company')),
                self._normalize_str(row.get('location')),
                date_posted,
                self._normalize_str(row.get('job_type')),
                self._normalize_str(row.get('salary_source')),
                self._normalize_str(row.get('interval')),
                float(row.get('min_amount')) if pd.notna(row.get('min_amount')) else None,
                float(row.get('max_amount')) if pd.notna(row.get('max_amount')) else None,
                self._normalize_str(row.get('currency')),
                bool(row.get('is_remote')) if pd.notna(row.get('is_remote')) else None,
                self._normalize_str(row.get('job_level')),
                self._normalize_str(row.get('job_function')),
                self._normalize_str(row.get('listing_type')),
                self._normalize_str(row.get('emails')),
                description_value,
                self._normalize_str(row.get('company_industry')),
                self._normalize_str(row.get('company_url')),
                self._normalize_str(row.get('company_logo')),
                self._normalize_str(row.get('company_url_direct')),
                self._normalize_str(row.get('company_addresses')),
                self._normalize_str(row.get('company_num_employees')),
                self._normalize_str(row.get('company_revenue')),
                self._normalize_str(row.get('company_description')),
                self._normalize_str(row.get('skills')),
                self._normalize_str(row.get('experience_range')),
                float(row.get('company_rating')) if pd.notna(row.get('company_rating')) else None,
                int(row.get('company_reviews_count')) if pd.notna(row.get('company_reviews_count')) else None,
                int(row.get('vacancy_count')) if pd.notna(row.get('vacancy_count')) else None,
                self._normalize_str(row.get('work_from_home_type')),
                seniority_level,
                role_family,
                primary_language,
                tech_tags,
                self._normalize_str(city_norm),
                self._normalize_str(country_norm),
            )
            jobs_data.append(job_tuple)

        # Filter out jobs that already exist or have no description
        new_jobs = []
        for job in jobs_data:
            job_id = job[0]
            description = job[19]  # description is at index 19 in the tuple
            
            # Skip if job already exists
            if self.job_exists(job_id):
                continue
                
            # Skip if description is empty, None, whitespace, or 'nan' (as string)
            if not description or (isinstance(description, str) and (not description.strip() or description.strip().lower() == 'nan')):
                logger.info(f"Skipping job {job_id} - no valid description provided")
                continue
                
            new_jobs.append(job)

        if not new_jobs:
            logger.info("No new jobs to insert")
            return 0

        insert_query = """
        INSERT INTO jobs (
            id, site, job_url, job_url_direct, title, company, location, date_posted,
            job_type, salary_source, interval, min_amount, max_amount, currency,
            is_remote, job_level, job_function, listing_type, emails, description,
            company_industry, company_url, company_logo, company_url_direct,
            company_addresses, company_num_employees, company_revenue, company_description,
            skills, experience_range, company_rating, company_reviews_count,
            vacancy_count, work_from_home_type,
            seniority_level, role_family, primary_language, tech_tags,
            city_normalized, country_normalized
        ) VALUES %s
        ON CONFLICT (id) DO NOTHING
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    execute_values(cur, insert_query, new_jobs)
                    conn.commit()
            logger.info(f"Successfully inserted {len(new_jobs)} new jobs")
            return len(new_jobs)
        except Exception as e:
            logger.error(f"Error inserting jobs: {e}")
            raise

    def cleanup_old_jobs(self, max_age_days):
        delete_query = """
        DELETE FROM jobs
        WHERE
            (date_posted IS NOT NULL AND date_posted < (CURRENT_DATE - %s))
            OR (date_posted IS NULL AND created_at < NOW() - (%s * INTERVAL '1 day'))
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(delete_query, (max_age_days, max_age_days))
                    deleted = cur.rowcount
                    conn.commit()
            logger.info(f"Deleted {deleted} jobs older than {max_age_days} days")
        except Exception as e:
            logger.error(f"Error cleaning up old jobs: {e}")

def scrape_and_save(config, db):
    """Scrape jobs for a single configuration and save to database"""
    try:
        logger.info(f"Starting scrape for query: {config['query_id']}")

        # Scrape jobs
        jobs = scrape_jobs(
            site_name=config['site_name'],
            search_term=config['search_term'],
            location=config.get('location'),
            results_wanted=config.get('results_wanted', 100),
            hours_old=config.get('hours_old', 72),
            country_indeed='USA',
            verbose=1
        )

        logger.info(f"Found {len(jobs)} jobs for {config['query_id']}")

        # Save to database
        if not jobs.empty:
            inserted_count = db.insert_jobs(jobs)
            logger.info(f"Inserted {inserted_count} new jobs for {config['query_id']}")
        else:
            logger.info(f"No jobs found for {config['query_id']}")

        # Add delay between scrapes to be respectful
        delay = config.get('delay', 2)
        if delay > 0:
            logger.info(f"Sleeping for {delay} seconds...")
            time.sleep(delay)

    except Exception as e:
        logger.error(f"Error scraping {config['query_id']}: {e}")
        # Continue with other configs even if one fails

def main(config_group="all"):
    """Main function to run scraping configurations

    Args:
        config_group: Which config group to run ('all', 'software_engineering', 'data_science', etc.)
    """
    logger.info(f"Starting job scraping workflow for group: {config_group}")

    # Get database connection string
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return

    # Initialize database
    db = JobDatabase(db_url)

    max_age_days_str = os.getenv('MAX_JOB_AGE_DAYS', '14')
    try:
        max_age_days = int(max_age_days_str)
    except ValueError:
        logger.error(f"Invalid MAX_JOB_AGE_DAYS value: {max_age_days_str}. Using default 14.")
        max_age_days = 14

    db.cleanup_old_jobs(max_age_days)

    # Get the appropriate config group
    if config_group not in CONFIG_GROUPS:
        logger.error(f"Unknown config group: {config_group}. Available: {list(CONFIG_GROUPS.keys())}")
        return

    configs = CONFIG_GROUPS[config_group]
    logger.info(f"Running {len(configs)} configurations for group '{config_group}'")

    # Run scraping configurations
    total_jobs = 0
    for config in configs:
        scrape_and_save(config, db)
        # Could track total jobs here if needed

    logger.info(f"Job scraping workflow completed for group: {config_group}")

if __name__ == "__main__":
    import sys
    config_group = sys.argv[1] if len(sys.argv) > 1 else "all"
    main(config_group)