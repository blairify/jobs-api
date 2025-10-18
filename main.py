import os
import logging
import pandas as pd
from datetime import datetime
from jobspy import scrape_jobs
from jobspy.config import SEARCH_CONFIGS
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_jobs_site ON jobs(site);
        CREATE INDEX IF NOT EXISTS idx_jobs_date_posted ON jobs(date_posted);
        CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
        CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
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
            if pd.notna(row.get('date_posted')):
                if isinstance(row['date_posted'], str):
                    try:
                        date_posted = datetime.strptime(row['date_posted'], '%Y-%m-%d').date()
                    except ValueError:
                        date_posted = None
                elif isinstance(row['date_posted'], datetime):
                    date_posted = row['date_posted'].date()

            job_tuple = (
                str(row.get('id', '')),
                str(row.get('site', '')),
                str(row.get('job_url', '')),
                str(row.get('job_url_direct', '')),
                str(row.get('title', '')),
                str(row.get('company', '')),
                str(row.get('location', '')),
                date_posted,
                str(row.get('job_type', '')),
                str(row.get('salary_source', '')),
                str(row.get('interval', '')),
                float(row.get('min_amount')) if pd.notna(row.get('min_amount')) else None,
                float(row.get('max_amount')) if pd.notna(row.get('max_amount')) else None,
                str(row.get('currency', '')),
                bool(row.get('is_remote')) if pd.notna(row.get('is_remote')) else None,
                str(row.get('job_level', '')),
                str(row.get('job_function', '')),
                str(row.get('listing_type', '')),
                str(row.get('emails', '')),
                str(row.get('description', '')),
                str(row.get('company_industry', '')),
                str(row.get('company_url', '')),
                str(row.get('company_logo', '')),
                str(row.get('company_url_direct', '')),
                str(row.get('company_addresses', '')),
                str(row.get('company_num_employees', '')),
                str(row.get('company_revenue', '')),
                str(row.get('company_description', '')),
                str(row.get('skills', '')),
                str(row.get('experience_range', '')),
                float(row.get('company_rating')) if pd.notna(row.get('company_rating')) else None,
                int(row.get('company_reviews_count')) if pd.notna(row.get('company_reviews_count')) else None,
                int(row.get('vacancy_count')) if pd.notna(row.get('vacancy_count')) else None,
                str(row.get('work_from_home_type', ''))
            )
            jobs_data.append(job_tuple)

        # Filter out jobs that already exist
        new_jobs = []
        for job in jobs_data:
            if not self.job_exists(job[0]):
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
            vacancy_count, work_from_home_type
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

def main():
    """Main function to run all scraping configurations"""
    logger.info("Starting job scraping workflow")

    # Get database connection string
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return

    # Initialize database
    db = JobDatabase(db_url)

    # Run all scraping configurations
    total_jobs = 0
    for config in SEARCH_CONFIGS:
        scrape_and_save(config, db)
        # Could track total jobs here if needed

    logger.info("Job scraping workflow completed")

if __name__ == "__main__":
    main()