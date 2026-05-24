class AlbumModel:
    def __init__(self, album_name, artist_name, year, label,
                 mood_description, cover_prompt, lastfm_tags):

        self.album_name = album_name
        self.artist_name = artist_name
        self.year = year
        self.label = label
        self.mood_description = mood_description
        self.cover_prompt = cover_prompt
        self.lastfm_tags = lastfm_tags

    def to_dict(self):
        album_info = {
            "album_name": self.album_name,
            "artist_name": self.artist_name,
            "year": self.year,
            "label": self.label,
            "mood_description": self.mood_description,
            "cover_prompt": self.cover_prompt,
            "lastfm_tags": self.lastfm_tags
        }

        return album_info

    def get_short_info(self):
        return self.album_name + " - " + self.artist_name + " (" + self.year + ")"

    def __str__(self):
        return self.get_short_info()
