
# worker_controller.py

import threading
from album_studio import (
    generate_album_metadata,
    build_tracklist,
    generate_cover_image,
)


class WorkerController:
    """
    GUI'den bağımsız arka plan iş kontrolcüsü.
    Tüm ağır işler (Gemini, Last.fm, görsel üretimi) burada yürütülür.
    """

    def __init__(self, on_status, on_result, on_error):
        """
        on_status : Callable[[str], None]  – durum mesajı callback'i
        on_result : Callable[[dict, list, Image], None]  – başarı callback'i
        on_error  : Callable[[str], None]  – hata callback'i
        """
        self.on_status = on_status
        self.on_result = on_result
        self.on_error  = on_error
        self._is_running = False

    # ── Public ────────────────────────────────────────────────────────────────

    @property
    def is_running(self):
        return self._is_running

    def start(self, journal: str, genre: str, era: str, track_count: int):
        """Arka plan thread'ini başlatır."""
        if self._is_running:
            return
        self._is_running = True
        threading.Thread(
            target=self._run,
            args=(journal, genre, era, track_count),
            daemon=True,
        ).start()

    # ── Private ───────────────────────────────────────────────────────────────

    def _run(self, journal: str, genre: str, era: str, track_count: int):
        try:
            self._set_status("🤖 Gemini is thinking...")
            album_data = generate_album_metadata(journal, genre, era, track_count)

            self._set_status("🎵 Fetching tracks from Last.fm...")
            tags = album_data.get("lastfm_tags", [])
            tracklist = build_tracklist(tags, track_count)
            if not tracklist:
                tracklist = build_tracklist([genre.lower()], track_count)
            album_data["tracklist"] = tracklist

            self._set_status("🎨 Generating cover art...")
            cover = generate_cover_image(
                album_data.get("cover_prompt", "abstract album cover")
            )

            self.on_result(album_data, tracklist, cover)

        except Exception as exc:
            self.on_error(str(exc))

        finally:
            self._is_running = False

    def _set_status(self, msg: str):
        self.on_status(msg)
