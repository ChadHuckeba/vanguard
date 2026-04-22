VAN_CONTRACT_INTERFACE
1.0 Overview
To facilitate the migration from state.json (Alpha) to SQLite (Beta), all data interactions must pass through a standardized Data Access Object (DAO). The ScoutCore will interact only with these methods, never the file system directly.
1.1 Mandatory Methods (Abstract)
METHOD: get_entry
Input: vanguard_id (String)
Output: PersistenceObject or Null (Includes all schema metadata)
Purpose: Retrieves a single entry for analysis or status updates.
METHOD: upsert_entry
Input: EntryObject (JSON/Dict)
Output: Boolean (Success/Fail)
Purpose: Handles new discovery ingestion and updating existing records (Deduplication).
METHOD: query_entries
Input: FilterCriteria (Dict: e.g., disposition, integrity_score)
Output: List of PersistenceObjects
Purpose: Retrieves entries based on status, integrity thresholds, or alignment scores.
METHOD: archive_expired
Input: TTL_Days (Integer, Default: 30)
Output: Integer (Total entries expired)
Purpose: Executes the State Decay logic to transition stale entries to the "Expired" disposition.
METHOD: backup_state
Input: None
Output: File Path (String)
Purpose: Executes the Atomic Write Protocol by generating a .bak snapshot before any data mutation.
1.2 Alpha Implementation: persistence_json.py
This is the active storage provider for Phase 1.
File Mapping: Directly manages I/O for state.json.
Lifecycle Logic: When upsert_entry is called, this provider checks the state.json for an existing ID. If found, it updates the last_seen timestamp and increments the hit_count.
Safety Protocol: Must execute the backup_state routine before any write mutation.
1.3 Beta Migration: persistence_sql.py
This is the planned storage provider for Phase 2.
File Mapping: Manages I/O for vanguard.db (SQLite).
Authority Mapping: Relational tables are generated based on the VAN_SCHEMA_PERSISTENCE at-rest authority.
Performance: Replaces linear JSON scans with indexed primary key lookups.

