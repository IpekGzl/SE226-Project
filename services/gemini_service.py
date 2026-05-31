import os
import json
import requests

from models.album_model import AlbumModel
from utils.json_cleaner import JsonCleaner


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("")

        self.api_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash-lite:generateContent"
        )

    def prepare_prompt(self, journal_text, genre, era, track_count):
        prompt = f"""
You are helping to design a fictional music album.

Use the journal entry below and create album metadata.

Return ONLY a valid JSON object.
Do not add any explanation before or after the JSON.

The JSON object must have these keys:
album_name, artist_name, year, label, mood_description, cover_prompt, lastfm_tags.

Rules:
- album_name, artist_name, year, and label must be fictional.
- Do not create song names or a tracklist.
- lastfm_tags must be a list of 4 to 6 lowercase music tags.
- cover_prompt must describe a square album cover image.
- The year must fit the selected era.

Journal entry:
{journal_text}

Selected genre:
{genre}

Selected era:
{era}

Number of tracks:
{track_count}
"""
        return prompt

    def convert_response_to_dict(self, raw_response):
        cleaner = JsonCleaner()
        cleaned_response = cleaner.clean_markdown_json(raw_response)

        try:
            album_data = json.loads(cleaned_response)
        except:
            raise ValueError("The Gemini response could not be converted to JSON.")

        required_fields = [
            "album_name",
            "artist_name",
            "year",
            "label",
            "mood_description",
            "cover_prompt",
            "lastfm_tags"
        ]

        for field in required_fields:
            if field not in album_data:
                raise ValueError("Missing album field: " + field)

        if not isinstance(album_data["lastfm_tags"], list):
            raise ValueError("lastfm_tags must be a list.")

        cleaned_tags = []

        for tag in album_data["lastfm_tags"]:
            clean_tag = str(tag).strip().lower()

            if clean_tag != "" and clean_tag not in cleaned_tags:
                cleaned_tags.append(clean_tag)

        if len(cleaned_tags) == 0:
            raise ValueError("There are no valid Last.fm tags.")

        album_data["lastfm_tags"] = cleaned_tags

        return album_data

    def make_album_object(self, album_data):
        album = AlbumModel(
            album_data["album_name"],
            album_data["artist_name"],
            album_data["year"],
            album_data["label"],
            album_data["mood_description"],
            album_data["cover_prompt"],
            album_data["lastfm_tags"]
        )

        return album

    def get_sample_year_for_era(self, era):
        if era == "1970s":
            return "1977"
        elif era == "1980s":
            return "1985"
        elif era == "1990s":
            return "1994"
        elif era == "2000s":
            return "2006"
        elif era == "2010s":
            return "2016"
        elif era == "2020s":
            return "2024"
        else:
            return "2024"

    def create_sample_album(self, journal_text="", genre="Indie", era="2010s"):
        text = journal_text.lower()
        year = self.get_sample_year_for_era(era)
        genre_lower = genre.lower()

        if "happy" in text or "dance" in text or "club" in text:
            album = AlbumModel(
                "City Lights After Midnight",
                "Nova Lane",
                year,
                "Silver Beat Records",
                "An energetic fictional album with bright city lights and dance feelings.",
                "A square album cover with neon lights, a crowded street, and people dancing.",
                [genre_lower, "dance pop", "electropop", "pop"]
            )

        elif "sad" in text or "lonely" in text or "tired" in text or "cry" in text:
            album = AlbumModel(
                "Letters I Never Sent",
                "Mira North",
                year,
                "Quiet Room Records",
                "A soft and emotional fictional album about loneliness, memories, and hope.",
                "A square album cover with old letters, rain on the window, and warm light.",
                [genre_lower, "dream pop", "indie folk", "alternative"]
            )

        elif "angry" in text or "dark" in text or "fight" in text:
            album = AlbumModel(
                "Static Heart",
                "The Broken Lines",
                year,
                "Red Noise Records",
                "A darker fictional album with intense sound and restless emotions.",
                "A square album cover with red street lights, broken glass, and a shadowy figure.",
                [genre_lower, "indie rock", "post-punk", "alternative rock"]
            )

        elif "sea" in text or "future" in text or "hopeful" in text:
            album = AlbumModel(
                "Waves Before Sunrise",
                "Elena Vale",
                year,
                "Blue Harbor Records",
                "A hopeful fictional album inspired by the sea, silence, and future dreams.",
                "A square album cover with a quiet sea, sunrise colors, and a person looking at the horizon.",
                [genre_lower, "dream pop", "lo-fi", "indie pop"]
            )

        else:
            album = AlbumModel(
                "Small Things",
                "Elena Vale",
                year,
                "Soft Echo Records",
                "A simple personal fictional album inspired by daily thoughts and quiet moments.",
                "A square album cover with headphones, a notebook, and soft bedroom light.",
                [genre_lower, "indie pop", "folk pop", "lo-fi"]
            )

        return album

    def generate_album_data(self, journal_text, genre, era, track_count):
        if not self.api_key:
            print("Gemini API key was not found. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)

        prompt = self.prepare_prompt(journal_text, genre, era, track_count)

        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        url = self.api_url + "?key=" + self.api_key

        try:
            response = requests.post(url, json=request_body, timeout=30)
        except:
            print("Could not connect to Gemini. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)

        if response.status_code == 429:
            print("Gemini quota problem occurred. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)

        if response.status_code != 200:
            print("Gemini returned an error. Sample album data is used.")
            print(response.text)
            return self.create_sample_album(journal_text, genre, era)

        try:
            response_data = response.json()
        except:
            print("Gemini response could not be read. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)

        try:
            raw_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            print("Gemini response format was not expected. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)

        try:
            album_data = self.convert_response_to_dict(raw_text)
            album = self.make_album_object(album_data)
            return album
        except:
            print("Gemini JSON format was wrong. Sample album data is used.")
            return self.create_sample_album(journal_text, genre, era)
