📜 VAN_CONTRACT_DEFINITIONS (Strategic/Tactical)
1.0 Purpose and Scope
This document serves as the high-authority map for all technical interfaces within the Vanguard ecosystem. Its primary goal is to maintain Modular Decoupling by defining the specific data "Handshakes" required for system interoperability.

2.0 The Discovery Contract (VAN_CONTRACT_DISCOVERY)
Role: The "Inbound" standard for data transmission.
Direction: Scout (Producer) → ScoutCore (Consumer).
Definition: A point-in-time snapshot of an Entry as it exists in the target environment.
Authority: Defines the mandatory fields - vanguard_id, source_metadata, and entry_content required for the Core to accept the data.
Constraint: The Scout is responsible for ID generation (SHA-256) and URL sanitization before transmission
3.0. The Persistence Schema (VAN_SCHEMA_PERSISTENCE)
Role: The "At-Rest" standard for long-term storage.
Direction: ScoutCore (Authority) ↔ state.json (Storage).
Definition: A cumulative record of an Entry's history, lifecycle, and system-level metadata.
Authority: Defines tracking fields that are invisible to the Scout, such as hit_count, last_seen, registration_metadata, and current disposition.
Constraint: Enforces the Atomic Write Protocol to prevent data corruption during local I/O operations
4.0 The Interface Contract (VAN_CONTRACT_INTERFACE)
Role: The "Functional" abstraction layer.
Direction: System Logic (User/Scout) → Data Access Object (DAO).
Definition: A standardized set of abstract methods that allow the system to interact with storage without knowing the underlying file format (JSON vs. SQL).
Authority: Defines mandatory methods such as upsert_entry, get_entry, and archive_expired.
Constraint: Facilitates the Bootstrap-First mandate by allowing a seamless pivot from state.json to SQLite in Phase 2.
