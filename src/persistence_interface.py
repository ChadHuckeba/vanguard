import os
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

class PersistenceInterface(ABC):
    """
    Abstract interface for state persistence to allow alpha-to-beta migration.
    All I/O must pass through this interface.
    """
    
    @abstractmethod
    def load_state(self) -> dict:
        """Loads the current global state from storage."""
        pass

    @abstractmethod
    def save_state(self, state: dict):
        """Saves the global state using an atomic write routine."""
        pass

class JSONPersistence(PersistenceInterface):
    """
    JSON implementation of the persistence interface.
    Follows the Atomic Write Protocol as defined in the SDD.
    """
    
    def __init__(self, state_path: Path):
        self.state_path = state_path
        self.bak_path = state_path.with_suffix(state_path.suffix + ".bak")
        self.tmp_path = state_path.with_suffix(state_path.suffix + ".tmp")

    def load_state(self) -> dict:
        if not self.state_path.exists():
            return None
        
        try:
            with open(self.state_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load state: {str(e)}")
            return None

    def save_state(self, state: dict):
        """
        Atomic Write Protocol:
        1. Rename state.json to state.json.bak.
        2. Write new data to state.tmp.
        3. Rename state.tmp to state.json upon success.
        """
        try:
            # 1. Backup existing state
            if self.state_path.exists():
                if self.bak_path.exists():
                    self.bak_path.unlink()
                os.rename(self.state_path, self.bak_path)
            
            # 2. Write to temporary file
            with open(self.tmp_path, 'w') as f:
                json.dump(state, f, indent=4)
            
            # 3. Rename tmp to final
            os.rename(self.tmp_path, self.state_path)
        except Exception as e:
            logging.error(f"Persistence Failure (Atomic Write Protocol): {str(e)}")
            # Try to recover if possible
            if self.tmp_path.exists() and not self.state_path.exists():
                os.rename(self.tmp_path, self.state_path)
