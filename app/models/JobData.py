from datetime import date
from pydantic import BaseModel
from pydantic import Field
from uuid import UUID
from app.models.WorkMode import WorkMode
from app.models.EmploymentType import EmploymentType
from app.models.ExperienceLevel import ExperienceLevel
from app.models.LookupValue import LookupValue

class JobData(BaseModel):
    id: UUID

    title: str = Field(min_length=1, max_length=100)
    company_name: str = Field(min_length=1, max_length=100)

    description: str = Field(min_length=1, max_length=20_000)

    location: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)

    work_mode: WorkMode
    employment_type: EmploymentType
    experience_level: ExperienceLevel

    industry: LookupValue
    department: LookupValue

    closing_date: date | None = None