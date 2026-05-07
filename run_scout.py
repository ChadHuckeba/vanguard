import sys
from pathlib import Path
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from jobspy_scout import JobSpyScout
from scout_core import core_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_research():
    print("--- VANGUARD: RESEARCH BRIDGE EXECUTION ---")
    print("Initializing JobSpyScout with Customer Support Manager (SaaS) context...")

    # Initialize the scout (loads config/scouts/jobspy.yaml by default)
    scout = JobSpyScout()

    print(f"Targeting: {scout.search_params.get('term')}")
    print(f"Engines: {', '.join(scout.search_params.get('sites'))}")
    print("Executing search passes (Remote + Local Austin/Pflugerville)...")

    try:
        scout.run()

        # Summary report
        results = core_engine.persistence.query_entries()
        print("\n--- EXECUTION SUMMARY ---")
        print(f"Total entries in DB: {len(results)}")

        # Show top 5 recent discoveries
        sorted_results = sorted(results, key=lambda x: x["metadata"]["last_seen"], reverse=True)
        print("\nTop 5 Recent Discoveries:")
        for job in sorted_results[:5]:
            title = job["content"].get("title")
            company = job["content"].get("company")
            location = job["content"].get("location")
            relo = job["content"].get("vanguard_relo_probability", 0.0)
            print(f"- {title} @ {company} [{location}] (Relo Prob: {relo})")

    except Exception as e:
        logging.error(f"Research run failed: {str(e)}")


if __name__ == "__main__":
    run_research()
