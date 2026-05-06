from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Company(BaseModel):
    company_name: str = Field(..., min_length=1)
    root_domain: Optional[str] = None
    career_url: Optional[str] = None
    ats_provider: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
