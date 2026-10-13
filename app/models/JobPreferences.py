from uuid import UUID
from pydantic import BaseModel
from pydantic import Field
from app.models.WorkMode import WorkMode
from app.models.EmploymentType import EmploymentType
from app.models.ExperienceLevel import ExperienceLevel
from app.models.LookupValue import LookupValue

class JobPreferences(BaseModel):
    id: UUID
    user_id: UUID

    preferred_title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    preferred_company_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    location: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    country: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    work_mode: WorkMode | None = None
    employment_type: EmploymentType | None = None
    experience_level: ExperienceLevel | None = None

    industry: LookupValue | None = None
    department: LookupValue | None = None