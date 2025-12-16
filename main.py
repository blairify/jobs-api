import os
import logging
import re
import pandas as pd
from jobspy import scrape_jobs
from jobspy.config import CONFIG_GROUPS
import psycopg2
from psycopg2.extras import execute_values
import time
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
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
            company_description TEXT,
            company_profile VARCHAR(50),
            skills TEXT,
            seniority_level VARCHAR(20),
            primary_language VARCHAR(50),
            tech_tags TEXT,
            city_normalized VARCHAR(100),
            country_normalized VARCHAR(100),
            position_tag VARCHAR(50),
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
            ADD COLUMN IF NOT EXISTS country_normalized VARCHAR(100),
            ADD COLUMN IF NOT EXISTS position_tag VARCHAR(50),
            ADD COLUMN IF NOT EXISTS company_profile VARCHAR(50);
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

    def _translate_text(self, text, target_lang="EN"):
        if not text:
            return None
        api_key = os.getenv("DEEPL_API_KEY")
        if not api_key:
            return None
        enabled = os.getenv("TRANSLATION_ENABLED", "false").lower() in (
            "1",
            "true",
            "yes",
        )
        if not enabled:
            return None
        api_url = os.getenv("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")
        try:
            response = requests.post(
                api_url,
                data={"auth_key": api_key, "text": text, "target_lang": target_lang},
                timeout=10,
            )
            if response.status_code != 200:
                logger.error(
                    f"Translation API error: {response.status_code} {response.text}"
                )
                return None
            data = response.json()
            translations = data.get("translations")
            if not translations:
                return None
            translated_text = translations[0].get("text")
            if not translated_text:
                return None
            return translated_text
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return None

    def _infer_seniority_level(self, title, description):
        text = f"{title or ''} {description or ''}".lower()
        text = re.sub(r"[^a-z0-9+#]+", " ", text)

        def _max_years_of_experience() -> int | None:
            years = []
            for m in re.finditer(r"\b(\d{1,2})\s*(?:\+)?\s*(?:years|yrs)\b", text):
                years.append(int(m.group(1)))
            for m in re.finditer(
                r"\b(\d{1,2})\s*(?:-|–|to)\s*(\d{1,2})\s*(?:years|yrs)\b",
                text,
            ):
                years.append(int(m.group(2)))
            return max(years) if years else None

        # Map to frontend enum values: entry, junior, mid, senior
        entry_patterns = [
            r"\b(intern|internship|apprentice|trainee)\b",
            r"\b(new\s*grad|graduate|recent\s*graduate)\b",
            r"\b(entry\s*level|entry\s*-\s*level)\b",
        ]
        junior_patterns = [
            r"\b(junior|jr\b|jr\.)\b",
            r"\b(associate)\b",
            r"\b(engineer|developer)\s*(i|1)\b",
            r"\b(level\s*(i|1))\b",
            r"\b(l1)\b",
        ]
        senior_patterns = [
            r"\b(senior|sr\b|sr\.)\b",
            r"\b(staff|principal|lead|architect)\b",
            r"\b(head\s+of)\b",
            r"\b(director|vp|vice\s+president|chief)\b",
            r"\b(engineering\s+manager|software\s+engineering\s+manager)\b",
        ]
        mid_patterns = [
            r"\b(mid\s*level|mid\s*-\s*level|intermediate)\b",
            r"\b(engineer|developer)\s*(ii|2|iii|3)\b",
            r"\b(level\s*(ii|2|iii|3))\b",
            r"\b(l2|l3)\b",
        ]

        if any(re.search(p, text) for p in entry_patterns):
            return "entry"
        if any(re.search(p, text) for p in junior_patterns):
            return "junior"
        if any(re.search(p, text) for p in senior_patterns):
            return "senior"
        if any(re.search(p, text) for p in mid_patterns):
            return "mid"

        years = _max_years_of_experience()
        if years is not None:
            if years <= 0:
                return "entry"
            if years <= 2:
                return "junior"
            if years <= 5:
                return "mid"
            return "senior"

        return "mid"

    def _infer_role_family(self, title, description):
        text = f"{title or ''} {description or ''}".lower()
        text = re.sub(r"[^a-z0-9+#]+", " ", text)

        product_patterns = [
            r"\b(product\s+manager|technical\s+product\s+manager|product\s+owner)\b",
            r"\b(group\s+product\s+manager|gpm)\b",
        ]
        cybersecurity_patterns = [
            r"\b(cyber\s*security|cybersecurity|info\s*sec|infosec|information\s+security)\b",
            r"\b(security\s+engineer|security\s+analyst|soc\s+analyst)\b",
            r"\b(penetration\s+tester|pentest|ethical\s+hacker|red\s+team|blue\s+team)\b",
            r"\b(application\s+security|appsec|vulnerability\s+management|incident\s+response)\b",
        ]
        data_scientist_patterns = [
            r"\b(data\s+scientist)\b",
            r"\b(machine\s+learning|ml\b|ml\s+engineer|ai\s+engineer|deep\s+learning)\b",
            r"\b(nlp|computer\s+vision|cv\b|llm|genai|generative\s+ai)\b",
            r"\b(applied\s+scientist|research\s+scientist)\b",
        ]
        data_engineering_patterns = [
            r"\b(data\s+engineer|analytics\s+engineer|etl\b|elt\b)\b",
            r"\b(data\s+pipeline|data\s+warehouse|data\s+platform)\b",
            r"\b(dbt|airflow|spark|kafka|snowflake|bigquery|redshift)\b",
            r"\b(bi\s+developer|business\s+intelligence)\b",
            r"\b(data\s+analyst|analytics)\b",
        ]
        devops_patterns = [
            r"\b(devops|site\s+reliability|sre\b|platform\s+engineer)\b",
            r"\b(infrastructure\s+engineer|infra\b|ci\s*/\s*cd|cicd)\b",
            r"\b(kubernetes|k8s|docker|terraform|ansible)\b",
            r"\b(cloud\s+engineer|cloud\s+architect|aws|azure|gcp)\b",
        ]
        mobile_patterns = [
            r"\b(mobile\s+developer|mobile\s+engineer)\b",
            r"\b(ios\b|android\b|react\s+native|flutter)\b",
            r"\b(swift|kotlin)\b",
        ]
        fullstack_patterns = [
            r"\b(full\s*stack|full\s*-\s*stack|fullstack|mern|mean)\b",
        ]
        frontend_patterns = [
            r"\b(front\s*end|front\s*-\s*end|frontend)\b",
            r"\b(ui\s+engineer|ui\s+developer|web\s+ui)\b",
            r"\b(react|next\s*js|angular|vue)\b",
        ]
        backend_patterns = [
            r"\b(back\s*end|back\s*-\s*end|backend)\b",
            r"\b(server\s*side|server\s*-\s*side)\b",
            r"\b(api\s+engineer|api\s+developer|microservices)\b",
        ]

        if any(re.search(p, text) for p in product_patterns):
            return "product"
        if any(re.search(p, text) for p in cybersecurity_patterns):
            return "security"
        if any(re.search(p, text) for p in data_scientist_patterns):
            return "data_scientist"
        if any(re.search(p, text) for p in data_engineering_patterns):
            return "data_engineer"
        if any(re.search(p, text) for p in devops_patterns):
            return "devops"
        if any(re.search(p, text) for p in mobile_patterns):
            return "mobile"
        if any(re.search(p, text) for p in fullstack_patterns):
            return "fullstack"
        if any(re.search(p, text) for p in frontend_patterns):
            return "frontend"
        if any(re.search(p, text) for p in backend_patterns):
            return "backend"

        return None

    def _infer_position_tag(self, title, description):
        title_text = (title or "").lower()
        desc_text = (description or "").lower()
        title_text = re.sub(r"[^a-z0-9+#]+", " ", title_text)
        desc_text = re.sub(r"[^a-z0-9+#]+", " ", desc_text)
        combined_text = f"{title_text} {desc_text}".strip()

        generic_title_markers = [
            r"\bsoftware\s+engineer\b",
            r"\bsoftware\s+developer\b",
            r"\bengineer\b",
            r"\bdeveloper\b",
        ]
        specific_role_markers = [
            r"\bfront\s*end\b",
            r"\bfrontend\b",
            r"\bback\s*end\b",
            r"\bbackend\b",
            r"\bfull\s*stack\b",
            r"\bfullstack\b",
            r"\bdevops\b",
            r"\bsre\b",
            r"\bmobile\b",
            r"\bios\b",
            r"\bandroid\b",
            r"\bdata\s+engineer\b",
            r"\bdata\s+scientist\b",
            r"\bproduct\s+manager\b",
            r"\bcybersecurity\b",
            r"\bsecurity\s+engineer\b",
        ]

        is_generic_title = any(re.search(p, title_text) for p in generic_title_markers)
        has_specific_title = any(
            re.search(p, title_text) for p in specific_role_markers
        )
        use_text = (
            desc_text
            if (is_generic_title and not has_specific_title)
            else combined_text
        )

        patterns_by_tag = {
            "cybersecurity": [
                r"\b(cyber\s*security|cybersecurity|info\s*sec|infosec|information\s+security)\b",
                r"\b(security\s+engineer|security\s+analyst|soc\s+analyst)\b",
                r"\b(penetration\s+tester|pentest|ethical\s+hacker|red\s+team|blue\s+team)\b",
                r"\b(application\s+security|appsec|devsecops|incident\s+response)\b",
                r"\b(vulnerability\s+management|threat\s+model(ing)?)\b",
            ],
            "product-manager": [
                r"\b(product\s+manager|product\s+owner)\b",
                r"\b(technical\s+product\s+manager|tpm)\b",
                r"\b(group\s+product\s+manager|gpm)\b",
            ],
            "data-scientist": [
                r"\b(data\s+scientist)\b",
                r"\b(machine\s+learning|ml\b|ml\s+engineer|ai\s+engineer|deep\s+learning)\b",
                r"\b(nlp|computer\s+vision|cv\b|llm|genai|generative\s+ai)\b",
                r"\b(applied\s+scientist|research\s+scientist)\b",
            ],
            "data": [
                r"\b(data\s+engineer|analytics\s+engineer|etl\b|elt\b)\b",
                r"\b(data\s+pipeline|data\s+warehouse|data\s+platform)\b",
                r"\b(dbt|airflow|spark|kafka|snowflake|bigquery|redshift)\b",
                r"\b(bi\s+developer|business\s+intelligence|data\s+analyst|analytics)\b",
            ],
            "devops": [
                r"\b(devops|site\s+reliability|sre\b|platform\s+engineer)\b",
                r"\b(infrastructure\s+engineer|infra\b|ci\s*/\s*cd|cicd)\b",
                r"\b(kubernetes|k8s|docker|terraform|ansible)\b",
                r"\b(cloud\s+engineer|cloud\s+architect|aws|azure|gcp)\b",
            ],
            "mobile": [
                r"\b(mobile\s+developer|mobile\s+engineer)\b",
                r"\b(ios\b|android\b|react\s+native|flutter)\b",
                r"\b(swift|kotlin)\b",
            ],
            "fullstack": [
                r"\b(full\s*stack|full\s*-\s*stack|fullstack|mern|mean)\b",
            ],
            "frontend": [
                r"\b(front\s*end|front\s*-\s*end|frontend)\b",
                r"\b(ui\s+engineer|ui\s+developer|web\s+ui)\b",
                r"\b(react|next\s*js|angular|vue)\b",
            ],
            "backend": [
                r"\b(back\s*end|back\s*-\s*end|backend)\b",
                r"\b(server\s*side|server\s*-\s*side)\b",
                r"\b(api\s+engineer|api\s+developer|microservices)\b",
                r"\b(django|flask|fastapi|spring\s+boot|rails|dotnet|\.net)\b",
            ],
        }

        matched = {
            tag
            for tag, patterns in patterns_by_tag.items()
            if any(re.search(p, use_text) for p in patterns)
        }

        if "cybersecurity" in matched:
            return "cybersecurity"
        if "product-manager" in matched:
            return "product-manager"
        if "data-scientist" in matched:
            return "data-scientist"

        if "fullstack" in matched or ("frontend" in matched and "backend" in matched):
            return "fullstack"

        if "devops" in matched:
            return "devops"
        if "mobile" in matched:
            return "mobile"
        if "data" in matched:
            return "data"
        if "frontend" in matched:
            return "frontend"
        if "backend" in matched:
            return "backend"

        return None

    def _infer_company_profile(
        self,
        company_name,
        company_industry,
        company_num_employees,
        company_description,
        job_description,
    ):
        text_parts = []
        for value in (
            company_name,
            company_industry,
            company_description,
            job_description,
        ):
            if value:
                text_parts.append(str(value))
        text = " ".join(text_parts).lower()

        # Detect FAANG-style companies
        faang_names = [
            "google",
            "meta",
            "facebook",
            "amazon",
            "apple",
            "netflix",
            "microsoft",
        ]
        if company_name:
            name_lower = str(company_name).strip().lower()
            if any(n in name_lower for n in faang_names):
                return "faang"
        if any(k in text for k in ["faang", "fang", "maang", "big tech"]):
            return "faang"

        # Detect startup-like companies
        size = None
        if company_num_employees:
            try:
                cleaned = "".join(
                    ch for ch in str(company_num_employees) if ch.isdigit()
                )
                if cleaned:
                    size = int(cleaned)
            except Exception:
                size = None
        if size is not None and size < 100:
            return "startup"
        if any(
            k in text
            for k in [
                "startup",
                "start-up",
                "seed stage",
                "seed-stage",
                "series a",
                "series b",
                "series c",
                "scale-up",
                "scale up",
            ]
        ):
            return "startup"

        # Default generic profile when we have some company context
        if text:
            return "generic"
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
            parts = [p.strip() for p in location.split(",") if p.strip()]
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
            raw_date = row.get("date_posted")
            if pd.notna(raw_date):
                try:
                    date_posted = pd.to_datetime(raw_date).date()
                except Exception:
                    date_posted = None

            title = row.get("title")
            raw_description = row.get("description")
            location = row.get("location")

            title_value = self._normalize_str(title)
            description_value = self._normalize_str(raw_description)

            source_title = title_value or title
            source_description = description_value or raw_description

            seniority_level = self._infer_seniority_level(
                source_title, source_description
            )
            position_tag = self._infer_position_tag(source_title, source_description)

            if not seniority_level or not position_tag:
                logger.info(
                    "Skipping job %s - missing seniority_level or position_tag",
                    row.get("id"),
                )
                continue

            primary_language, tech_tags = self._extract_tech_tags(
                source_title, source_description
            )
            city_norm, country_norm = self._normalize_location_parts(location)

            company_name = self._normalize_str(row.get("company"))
            company_industry = self._normalize_str(row.get("company_industry"))

            company_description_value = self._normalize_str(
                row.get("company_description")
            )
            company_profile = self._infer_company_profile(
                company_name,
                company_industry,
                company_description_value,
                description_value,
            )

            job_tuple = (
                str(row.get("id", "")),
                str(row.get("site", "")),
                str(row.get("job_url", "")),
                str(row.get("job_url_direct", "")),
                str(row.get("title", "")),
                company_name,
                self._normalize_str(row.get("location")),
                date_posted,
                self._normalize_str(row.get("job_type")),
                self._normalize_str(row.get("salary_source")),
                float(row.get("min_amount"))
                if pd.notna(row.get("min_amount"))
                else None,
                float(row.get("max_amount"))
                if pd.notna(row.get("max_amount"))
                else None,
                self._normalize_str(row.get("currency")),
                bool(row.get("is_remote")) if pd.notna(row.get("is_remote")) else None,
                self._normalize_str(row.get("job_level")),
                self._normalize_str(row.get("job_function")),
                self._normalize_str(row.get("listing_type")),
                self._normalize_str(row.get("emails")),
                description_value,
                self._normalize_str(row.get("company_industry")),
                self._normalize_str(row.get("company_url")),
                self._normalize_str(row.get("company_logo")),
                self._normalize_str(row.get("company_url_direct")),
                self._normalize_str(row.get("company_addresses")),
                self._normalize_str(row.get("company_description")),
                self._normalize_str(row.get("skills")),
                seniority_level,
                primary_language,
                tech_tags,
                self._normalize_str(city_norm),
                self._normalize_str(country_norm),
                position_tag,
                company_profile,
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
            if not description or (
                isinstance(description, str)
                and (not description.strip() or description.strip().lower() == "nan")
            ):
                logger.info(f"Skipping job {job_id} - no valid description provided")
                continue

            new_jobs.append(job)

        if not new_jobs:
            logger.info("No new jobs to insert")
            return 0

        insert_query = """
        INSERT INTO jobs (
            id, site, job_url, job_url_direct, title, company, location, date_posted,
            job_type, salary_source, min_amount, max_amount, currency,
            is_remote, job_level, job_function, listing_type, emails, description,
            company_industry, company_url, company_logo, company_url_direct,
            company_description,
            skills, seniority_level, primary_language, tech_tags,
            city_normalized, country_normalized, position_tag, company_profile
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


def infer_country_indeed(location):
    """Infer JobSpy's country_indeed parameter from a human-readable location.

    Examples:
    - "San Francisco, CA" -> "USA"
    - "New York, NY" -> "USA"
    - "London, United Kingdom" -> "UK"
    - "Berlin, Germany" -> "Germany"
    - "Warsaw, Poland" -> "Poland"
    Falls back to "USA" when unsure, so US workflows keep working.
    """
    if not location:
        return "USA"

    if isinstance(location, str):
        parts = [p.strip() for p in location.split(",") if p.strip()]
        if not parts:
            return "usa"

        last = parts[-1]
        last_lower = last.lower()

        # Explicit US markers
        if last_lower in ("united states", "usa", "us"):
            return "usa"

        # Two-letter region like "CA", "NY" etc. -> assume US state
        if len(last) == 2 and last.isupper():
            return "usa"

        # Map common UK spellings to the code JobSpy expects
        if last_lower in (
            "united kingdom",
            "england",
            "scotland",
            "wales",
            "northern ireland",
        ):
            return "uk"

        # Otherwise, use the country name lower-cased (e.g. "germany", "poland",
        # "czech republic") to match JobSpy's expected country_indeed strings.
        return last_lower

    return "usa"


def scrape_and_save(config, db):
    """Scrape jobs for a single configuration and save to database"""
    try:
        logger.info(f"Starting scrape for query: {config['query_id']}")

        # Derive country_indeed per config so international locations
        # (e.g. EU capitals) query the correct Indeed country endpoint.
        location = config.get("location")
        country_indeed = config.get("country_indeed")
        if not country_indeed:
            country_indeed = infer_country_indeed(location)

        # Enable full LinkedIn descriptions where applicable so jobs
        # aren't skipped just because the brief listing view omits them.
        site_name = config["site_name"]
        has_linkedin = False
        if isinstance(site_name, str):
            has_linkedin = site_name.lower() == "linkedin"
        else:
            has_linkedin = any(s.lower() == "linkedin" for s in site_name)

        # Scrape jobs
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=config["search_term"],
            location=location,
            results_wanted=config.get("results_wanted", 100),
            hours_old=config.get("hours_old", 72),
            country_indeed=country_indeed,
            linkedin_fetch_description=has_linkedin,
            verbose=1,
        )

        logger.info(f"Found {len(jobs)} jobs for {config['query_id']}")

        # Save to database
        if not jobs.empty:
            inserted_count = db.insert_jobs(jobs)
            logger.info(f"Inserted {inserted_count} new jobs for {config['query_id']}")
        else:
            logger.info(f"No jobs found for {config['query_id']}")

        # Add delay between scrapes to be respectful
        delay = config.get("delay", 2)
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
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return

    # Initialize database
    db = JobDatabase(db_url)

    max_age_days_str = os.getenv("MAX_JOB_AGE_DAYS", "7")
    try:
        max_age_days = int(max_age_days_str)
    except ValueError:
        logger.error(
            f"Invalid MAX_JOB_AGE_DAYS value: {max_age_days_str}. Using default 7."
        )
        max_age_days = 7

    db.cleanup_old_jobs(max_age_days)

    # Get the appropriate config group
    if config_group not in CONFIG_GROUPS:
        logger.error(
            f"Unknown config group: {config_group}. Available: {list(CONFIG_GROUPS.keys())}"
        )
        return

    configs = CONFIG_GROUPS[config_group]
    logger.info(f"Running {len(configs)} configurations for group '{config_group}'")

    # Run scraping configurations
    for config in configs:
        scrape_and_save(config, db)
        # Could track total jobs here if needed

    logger.info(f"Job scraping workflow completed for group: {config_group}")


if __name__ == "__main__":
    import sys

    config_group = sys.argv[1] if len(sys.argv) > 1 else "all"
    main(config_group)
