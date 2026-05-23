class Deduplicator:

    def remove_duplicate_tracks(self, tracks):

        unique_tracks = []

        seen = []

        for track in tracks:

            key = (
                track.title.lower(),
                track.artist.lower()
            )

            if key not in seen:

                seen.append(key)

                unique_tracks.append(track)

        return unique_tracks
