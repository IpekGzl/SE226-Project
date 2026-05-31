# gui/app_window.py

import tkinter as tk
from tkinter import ttk

from models.app_state import AppState
from gui.input_panel import InputPanel
from gui.album_panel import AlbumPanel
from gui.status_manager import StatusManager
from controllers.album_controller import AlbumController
from controllers.worker_controller import WorkerController

# Spotify-style Renk Paleti Tasarımı
BG_DARK = "#0d0d0d"
BG_CARD = "#181818"
ACCENT = "#1db954"
TEXT_PRI = "#ffffff"
BORDER = "#282828"


class AppWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Album Cover Studio")
        self.geometry("1050x750")
        self.minsize(900, 650)
        self.configure(bg=BG_DARK)

        # Temel Durum ve İş Kontrolörleri Tanımlamaları
        self.state = AppState()
        self.worker_controller = WorkerController(self)
        self.album_controller = AlbumController(self)

        self._setup_styles()
        self._setup_layout()

    def _setup_styles(self) -> None:
        """Tüm uygulamanın modern Spotify tarzı görünmesini sağlayan stil konfigürasyonları."""
        style = ttk.Style()
        style.theme_use("default")

        # Genel Bileşen Stilleri
        style.configure("TFrame", background=BG_DARK)
        style.configure("Card.TFrame", background=BG_CARD, borderwidth=1, relief="solid")

        style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRI, font=("Helvetica", 10))
        style.configure("Accent.TLabel", background=BG_CARD, foreground=ACCENT, font=("Helvetica", 11, "bold"))
        style.configure("Dim.TLabel", background=BG_CARD, foreground="#b3b3b3", font=("Helvetica", 9))

        # Buton Stilleri
        style.configure("Accent.TButton", background=ACCENT, foreground=TEXT_PRI, font=("Helvetica", 10, "bold"),
                        borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#158a3e"), ("disabled", "#282828")])

        style.configure("Secondary.TButton", background="#282828", foreground=TEXT_PRI, font=("Helvetica", 9, "bold"),
                        borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#3e3e3e")])

    def _setup_layout(self) -> None:
        """Panelleri ekrana yerleştirir ve aralarındaki bağları kurar."""
        # Sol Taraf: Input Panel (Veri giriş alanları)
        # InputPanel bizden bir on_generate callback fonksiyonu bekler.
        self.input_panel = InputPanel(self, on_generate=self._handle_generate_request)

        # Sağ Taraf: Albüm Görünüm Paneli (Kapak imajı ve Şarkı tablosu)
        self.album_panel = AlbumPanel(self)
        self.album_panel.pack(side="right", fill="both", expand=True, padx=(0, 16), pady=16)

        # Alt Bölüm: Export (Kaydet) Butonu Ekleme (AlbumPanel altına yerleşim)
        export_btn = ttk.Button(
            self.album_panel,
            text="EXPORT ALBUM (JSON + PNG)",
            style="Secondary.TButton",
            command=self.album_controller.trigger_export
        )
        export_btn.pack(side="bottom", fill="x", padx=15, pady=10)

        # Durum yöneticisini InputPanel'deki değişkenler üzerinden bağlıyoruz
        self.status_manager = StatusManager(
            status_var=self.input_panel.status_var,
            gen_btn=self.input_panel.gen_btn
        )

    def _handle_generate_request(self, journal_text: str, genre: str, era: str, track_count: int) -> None:
        """Giriş panelinden gelen üretim tetiklemesini thread'e devreder."""
        self.status_manager.set_generating()

        # UI freeze yaşamamak için pipeline'ı WorkerController yardımıyla arka planda başlatıyoruz
        self.worker_controller.start_generation_thread(
            lambda: self.album_controller.generate_album_pipeline(journal_text, genre, era, track_count)
        )
