from pydantic import BaseModel
from pydantic import Field

class MatchFeatures(BaseModel):
    title_similarity: float | None = Field(default=None, ge=0.0, le=1.0)
    company_similarity: float | None = Field(default=None, ge=0.0, le=1.0)
    location_similarity: float | None = Field(default=None, ge=0.0, le=1.0)
    country_match: float | None = Field(default=None, ge=0.0, le=1.0)
    work_mode_match: float | None = Field(default=None, ge=0.0, le=1.0)
    employment_type_match: float | None = Field(default=None, ge=0.0, le=1.0)
    experience_level_match: float | None = Field(default=None, ge=0.0, le=1.0)
    industry_match: float | None = Field(default=None, ge=0.0, le=1.0)
    department_match: float | None = Field(default=None, ge=0.0, le=1.0)