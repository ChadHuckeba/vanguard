import logging
import sys
import os
import sqlite3
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from persistence_interface import SQLitePersistence
from utils.career_page_parser import CareerPageParser

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("vanguard.migration")

def backfill_career_urls():
    """
    Iterates through existing entries and attempts to extract career URLs.
    """
    db_path = Path("/home/chadh/survivalstack/Vanguard/data/vanguard.db")
    if not db_path.exists():
        logger.error(f"Database not found at {db_path}")
        return

    # Initialize persistence to trigger migrations
    persistence = SQLitePersistence(db_path)
    
    # Query all entries that are 'pending' or have NULL career_url
    with persistence._get_connection() as conn:
        rows = conn.execute("""
            SELECT vanguard_id, entry_data, provider_id 
            FROM entries 
            WHERE career_extraction_status = 'pending' OR career_url IS NULL
        """).fetchall()

    if not rows:
        logger.info("No entries require career URL backfill.")
        return

    logger.info(f"Starting backfill for {len(rows)} entries...")

    for row in rows:
        v_id = row["vanguard_id"]
        entry_data = row["entry_data"]
        # In a real scenario, we might need a company domain scout to find the career page first.
        # For this Alpha retrofit, we'll try to guess/extract from the entry_data or source.
        # Most JobSpy data has a 'company_url' or we can derive it.
        
        import json
        data = json.loads(entry_data)
        
        # 1. Try to find a career page candidate
        # Priority: explicit company_url > deriving from email/source
        target_site = data.get("company_url") or data.get("source_url")
        
        if not target_site or "linkedin.com" in target_site or "indeed.com" in target_site:
            # If it's a job board URL, we can't easily find the career page without more logic
            # Mark as failed for now so we can identify these in the dashboard
            persistence.upsert_entry({
                "vanguard_id": v_id,
                "career_info": {
                    "status": "failed",
                    "error": "No direct company URL available for extraction"
                }
            })
            continue

        # 2. Run Parser
        parser = CareerPageParser(target_site)
        result = parser.extract_job_urls()
        
        # 3. Update DB
        persistence.upsert_entry({
            "vanguard_id": v_id,
            "career_info": {
                "url": result["urls"][0] if result["urls"] else None,
                "method": result["method"],
                "status": result["status"],
                "error": result["error"]
            }
        })
        logger.info(f"Processed {v_id[:8]}: {result['status'].upper()}")

if __name__ == "__main__":
    backfill_career_urls()
