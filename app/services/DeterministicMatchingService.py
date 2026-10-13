from app.models.JobData import JobData
from app.models.JobPreferences import JobPreferences


class DeterministicMatchingService:
    
    @staticmethod
    def exact_match(preference, actual) -> float | None:
        if preference is None:
            return None
        return 1.0 if preference == actual else 0.0

    @staticmethod
    def lookup_match(preference, actual) -> float | None:
        if preference is None:
            return None
        return 1.0 if preference.id == actual.id else 0.0

    def calculate_features(
        self,
        preferences: JobPreferences,
        job: JobData,
    ) -> dict[str, float | None]:
        return {
            "country_match": self.exact_match(
                preferences.country, job.country
            ),
            "location_similarity": self.exact_match(
                preferences.location, job.location
            ),
            "work_mode_match": self.exact_match(
                preferences.work_mode, job.work_mode
            ),
            "employment_type_match": self.exact_match(
                preferences.employment_type, job.employment_type
            ),
            "experience_level_match": self.exact_match(
                preferences.experience_level, job.experience_level
            ),
            "industry_match": self.lookup_match(
                preferences.industry, job.industry
            ),
            "department_match": self.lookup_match(
                preferences.department, job.department
            ),
        }
