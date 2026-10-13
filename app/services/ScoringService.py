from app.models.MatchFeatures import MatchFeatures


class ScoringService:

    WEIGHTS = {
        "title_similarity": 0.25,
        "company_similarity": 0.05,
        "location_similarity": 0.10,
        "country_match": 0.10,
        "work_mode_match": 0.15,
        "employment_type_match": 0.10,
        "experience_level_match": 0.10,
        "industry_match": 0.10,
        "department_match": 0.05,
    }

    def calculate(
        self,
        features: MatchFeatures,
    ) -> float:

        weighted_score = 0.0
        active_weight = 0.0

        values = features.model_dump()

        for feature_name, weight in self.WEIGHTS.items():

            value = values[feature_name]

            if value is None:
                continue

            weighted_score += value * weight
            active_weight += weight

        if active_weight == 0:
            return 0.0

        normalized_score = (
            weighted_score / active_weight
        )

        return round(
            normalized_score * 100,
            2,
        )
        

def get_match_level(score: float) -> str:

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Strong"

    if score >= 50:
        return "Moderate"

    return "Low"