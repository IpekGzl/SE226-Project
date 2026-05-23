from tkinter import messagebox

from services.gemini_service import GeminiService
from services.lastfm_service import LastFmService
from services.image_service import ImageService

from gui.album_panel import AlbumPanel


class AlbumController:

    def __init__(self, app):

        self.app = app

        self.gemini_service = GeminiService()
        self.lastfm_service = LastFmService()
        self.image_service = ImageService()

    def generate_album_pipeline(
        self,
        journal_text: str,
        genre: str,
        era: str,
        track_count: int
    ) -> None:

        try:

            self.app.status_manager.update_status(
                "Gemini is thinking..."
            )

            album_data = self.gemini_service.generate_album_data(
                journal_text,
                genre,
                era,
                track_count
            )

            self.app.status_manager.update_status(
                "Fetching tracks..."
            )

            tracks = self.lastfm_service.build_tracklist(
                album_data.lastfm_tags,
                track_count
            )

            self.app.status_manager.update_status(
                "Generating cover..."
            )

            image = self.image_service.generate_cover_image(
                album_data.cover_prompt
            )

            self.app.status_manager.update_status(
                "Updating UI..."
            )

            self.app.album_panel.update_album(
                album_data,
                tracks,
                image
            )

            self.app.status_manager.update_status(
                "Done!"
            )

        except Exception as e:

            self.handle_generation_error(e)

    def handle_generation_error(
        self,
        error: Exception
    ) -> None:

        messagebox.showerror(
            "Generation Error",
            str(error)
        )

        self.app.status_manager.update_status(
            "Error occurred."
        )
