import requests

from models.track_model import TrackModel
from utils.deduplicator import Deduplicator


class LastFmService:

    BASE_URL = "https://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key):

        self.api_key = api_key

    def fetch_tracks_by_tag(self, tag, limit=20):

        params = {
            "method": "tag.gettoptracks",
            "tag": tag,
            "limit": limit,
            "api_key": self.api_key,
            "format": "json"
        }

        headers = {
            "User-Agent": "PDA226/1.0"
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            headers=headers
        )

        data = response.json()

        tracks = data["tracks"]["track"]

        return tracks

    def convert_to_track_model(self, raw_track):

        title = raw_track["name"]

        artist = raw_track["artist"]["name"]

        url = raw_track["url"]

        track = TrackModel(
            title,
            artist,
            url
        )

        return track

    def build_tracklist(self, tags, requested_count):

        all_tracks = []

        for tag in tags:

            try:

                raw_tracks = self.fetch_tracks_by_tag(
                    tag,
                    requested_count
                )

                for raw_track in raw_tracks:

                    track = self.convert_to_track_model(
                        raw_track
                    )

                    all_tracks.append(track)

            except Exception as error:

                print(error)

        deduplicator = Deduplicator()

        unique_tracks = (
            deduplicator.remove_duplicate_tracks(
                all_tracks
            )
        )

        final_tracks = unique_tracks[
            :requested_count
        ]

        return final_tracks
