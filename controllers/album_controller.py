# controllers/album_controller.py

from tkinter import messagebox
from services.gemini_service import GeminiService
from services.lastfm_service import LastFmService
from services.image_service import ImageService
from services.export_service import ExportService
from config import LASTFM_API_KEY

class AlbumController:
    def __init__(self, app):
        self.app = app
        self.gemini_service = GeminiService()
        # LastFmService config'deki api_key'i bekliyor
        self.lastfm_service = LastFmService(api_key=LASTFM_API_KEY)
        self.image_service = ImageService()
        self.export_service = ExportService()

    def generate_album_pipeline(self, journal_text: str, genre: str, era: str, track_count: int) -> None:
        """Arka planda çalışacak olan veri üretim hattı (pipeline)."""
        try:
            # 1. Aşama: Gemini ile Metadata Üretimi
            self.app.worker_controller.safe_ui_callback(
                self.app.status_manager.set_status, "⏳ Gemini is thinking..."
            )
            album_data = self.gemini_service.generate_album_data(
                journal_text, genre, era, track_count
            )
            self.app.state.album = album_data

            # 2. Aşama: Last.fm ile Şarkı Listesi Oluşturma
            self.app.worker_controller.safe_ui_callback(
                self.app.status_manager.set_status, "⏳ Fetching tracks from Last.fm..."
            )
            tracks = self.lastfm_service.build_tracklist(
                album_data.lastfm_tags, track_count
            )
            self.app.state.tracks = tracks

            # 3. Aşama: Pollinations ile Kapak Görseli Oluşturma
            self.app.worker_controller.safe_ui_callback(
                self.app.status_manager.set_status, "⏳ Generating cover image..."
            )
            # İmaj stilini zenginleştirmek için prompt'u build ediyoruz
            final_prompt = self.image_service.build_cover_prompt(album_data.cover_prompt, genre)
            image = self.image_service.generate_cover_image(final_prompt)
            self.app.state.cover_image = image

            # 4. Aşama: Arayüzü Güvenli Şekilde Güncelleme
            self.app.worker_controller.safe_ui_callback(
                self.app.album_panel.update_album, album_data, tracks, image
            )
            self.app.worker_controller.safe_ui_callback(
                self.app.status_manager.set_done, len(tracks)
            )

        except Exception as e:
            self.app.worker_controller.safe_ui_callback(self.handle_generation_error, e)

    def handle_generation_error(self, error: Exception) -> None:
        messagebox.showerror("Generation Error", f"Something went wrong:\n{str(error)}")
        self.app.status_manager.set_error(str(error))

    def trigger_export(self) -> None:
        """Mevcut albüm durumunu export etmek için kullanılır."""
        if not self.app.state.album or not self.app.state.cover_image:
            messagebox.showwarning("Nothing to Save", "Please generate an album first.")
            return

        output_dir = self.export_service.choose_export_directory()
        if not output_dir:
            return

        try:
            json_path = self.export_service.export_album_json(self.app.state.album.to_dict(), output_dir)
            png_path = self.export_service.export_cover_png(self.app.state.cover_image, output_dir)
            messagebox.showinfo("Export Successful", f"Saved successfully!\n\nJSON: {json_path}\nPNG: {png_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export files:\n{str(error)}")
