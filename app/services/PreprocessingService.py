class PreprocessingService:

    @staticmethod
    def normalize_text(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = " ".join(
            value.strip().lower().split()
        )

        return normalized or None