from uuid import UUID
from pydantic import BaseModel

class LookupValue(BaseModel):
    id: UUID
    name: str
