import sys
import os
import shutil
import json
from pathlib import Path

# Add src to python path
root_dir = Path(__file__).parent.parent
src_path = root_dir / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from scout_core import ScoutCore
from persistence_interface import SQLitePersistence

def setup_test_env():
    """Wipes test data to ensure clean run."""
    test_data_dir = root_dir / "data_test"
    if test_data_dir.exists():
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir()
    return test_data_dir

def test_sqlite_direct():
    print("\n--- [1] Testing SQLite Direct Operations ---")
    db_path = root_dir / "data_test" / "test_vanguard.db"
    sql_prov = SQLitePersistence(db_path)
    
    mock_entry = {
        "vanguard_id": "test_id_123",
        "source_info": {"scout": "TestScout", "source_url": "http://test.com"},
        "content": {"title": "Test Engineer", "salary": "100k"},
        "metadata": {"hit_count": 1}
    }
    
    # Test Upsert
    sql_prov.upsert_entry(mock_entry)
    print("✓ Upsert successful.")
    
    # Test Retrieval
    retrieved = sql_prov.get_entry("test_id_123")
    assert retrieved["vanguard_id"] == "test_id_123"
    assert retrieved["content"]["title"] == "Test Engineer"
    assert retrieved["metadata"]["hit_count"] == 1
    print("✓ Data retrieval and reconstruction successful.")
    
    # Test Hit Count Increment
    sql_prov.upsert_entry(mock_entry)
    retrieved_again = sql_prov.get_entry("test_id_123")
    assert retrieved_again["metadata"]["hit_count"] == 2
    print("✓ Hit count increment verified.")

def test_migration_logic():
    print("\n--- [2] Testing Legacy JSON Migration ---")
    
    # Reset Singleton for testing
    ScoutCore._instance = None
    ScoutCore._initialized = False
    
    test_dir = root_dir / "data_test"
    json_path = test_dir / "state.json"
    db_path = test_dir / "vanguard.db"
    
    # Create legacy JSON
    legacy_data = {
        "state_metadata": {"version": "1.0", "total_records": 1},
        "entities": {
            "legacy_id_999": {
                "vanguard_id": "legacy_id_999",
                "label": "Legacy Lead",
                "source": "http://old-source.com",
                "metadata": {"hit_count": 5, "first_seen": "2026-01-01T00:00:00Z", "last_seen": "2026-01-01T00:00:00Z"},
                "data": {"note": "migrated"}
            }
        }
    }
    with open(json_path, 'w') as f:
        json.dump(legacy_data, f)
    
    # Initialize Core (should trigger migration)
    # Patch ScoutCore to use test paths
    class TestScoutCore(ScoutCore):
        def _initialize_core(self):
            print(f"DEBUG: Initializing TestScoutCore with data_dir: {root_dir / 'data_test'}")
            self.root_dir = root_dir
            self.data_dir = root_dir / "data_test"
            self.state_path = self.data_dir / "state.json"
            self.db_path = self.data_dir / "vanguard.db"
            self.log_path = root_dir / "logs" / "test_system.log"
            self.data_dir.mkdir(exist_ok=True)
            self.persistence = SQLitePersistence(self.db_path)
            print(f"DEBUG: state_path exists: {self.state_path.exists()}")
            if self.state_path.exists():
                self._migrate_from_json()

    core = TestScoutCore()
    
    # Verify migration results
    print("DEBUG: Checking database for legacy_id_999...")
    entry = core.persistence.get_entry("legacy_id_999")
    if entry is None:
        print("DEBUG: Entry legacy_id_999 not found in DB.")
        all_entries = core.persistence.query_entries()
        print(f"DEBUG: All entries in DB: {[e['vanguard_id'] for e in all_entries]}")
        
    assert entry is not None
    assert entry["metadata"]["hit_count"] == 5
    assert entry["content"]["title"] == "Legacy Lead"
    print("✓ Migration integrity verified.")
    
    # Verify file handling
    assert not json_path.exists()
    assert (test_dir / "state.json.migrated").exists()
    print("✓ Legacy file cleanup verified.")

if __name__ == "__main__":
    try:
        setup_test_env()
        test_sqlite_direct()
        test_migration_logic()
        print("\nALL PRE-MERGE TESTS PASSED 🚀")
    except Exception as e:
        print(f"\n❌ TEST FAILURE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup
        test_data_dir = root_dir / "data_test"
        if test_data_dir.exists():
             shutil.rmtree(test_data_dir)
