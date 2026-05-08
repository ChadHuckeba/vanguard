from typing import Optional, List
from pydantic import BaseModel, field_validator


# Centralized list of job aggregators and third-party boards to block from official discovery
GLOBAL_AGGREGATOR_BLOCKLIST: List[str] = [
    "jooble.org",
    "lensa.com",
    "swooped.co",
    "monster.com",
    "dice.com",
    "salary.com",
    "levels.fyi",
    "swooped.app",  # Added to catch the Swooped app variant
]


def is_blocked_url(url: str) -> bool:
    """Utility to check if a URL belongs to a blocked aggregator."""
    if not url:
        return False
    url_lower = url.lower()
    return any(blocked in url_lower for blocked in GLOBAL_AGGREGATOR_BLOCKLIST)


class DiscoveryResult(BaseModel):
    portal_url: Optional[str] = None
    deep_link: Optional[str] = None
    status: str = "pending"
    method: Optional[str] = None
    error: Optional[str] = None
    confidence_score: float = 0.0

    @field_validator("portal_url", "deep_link")
    @classmethod
    def check_not_blocked(cls, v: Optional[str]) -> Optional[str]:
        if v and is_blocked_url(v):
            raise ValueError(f"URL matches a blocked aggregator domain: {v}")
        return v
