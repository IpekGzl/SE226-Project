class Validators:

    @staticmethod
    def validate_journal_text(
        text: str
    ) -> bool:

        return bool(text and text.strip())

    @staticmethod
    def validate_track_count(
        count: int
    ) -> bool:

        return 1 <= count <= 50

    @staticmethod
    def validate_genre(
        genre: str
    ) -> bool:

        return bool(genre and genre.strip())

    @staticmethod
    def validate_era(
        era: str
    ) -> bool:

        return bool(era and era.strip())

    @staticmethod
    def validate_url(
        url: str
    ) -> bool:

        return url.startswith("http://") or url.startswith("https://")
