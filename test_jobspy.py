import csv
from jobspy import scrape_jobs

# Simple test to scrape a few jobs
jobs = scrape_jobs(
    site_name=["indeed"],  # Start with one site to avoid rate limits
    search_term="software engineer",
    location="San Francisco, CA",
    results_wanted=5,  # Small number for quick test
    hours_old=72,
    country_indeed='USA',
    verbose=2  # Show all logs
)

print(f"Found {len(jobs)} jobs")
if len(jobs) > 0:
    print(jobs.head())
    jobs.to_csv("test_jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    print("Results saved to test_jobs.csv")
else:
    print("No jobs found")