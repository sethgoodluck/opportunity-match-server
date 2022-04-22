from pydantic import BaseModel
from typing import Optional

class Opportunity(BaseModel):
    id: int
    organization: str
    roles: list[str]
    email: Optional[str]

class User(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    interested_in: Optional[list[str]]