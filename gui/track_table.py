# gui/track_table.py

import tkinter as tk
from tkinter import ttk

from utils.browser_utils import BrowserUtils


class TrackTable(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.track_buttons = []
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # İçteki frame'i canvas'a ekleyip ID'sini alıyoruz
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        # EKRAN GENİŞLEDİKÇE FRAME'İN DE GENİŞLEMESİNİ SAĞLAYAN KRİTİK KOD:
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def render_tracks(self, tracks) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.track_buttons.clear()

        # Grid yapısı için sütunların genişleme ağırlıklarını (weight) belirliyoruz
        self.scrollable_frame.columnconfigure(1, weight=3)  # Title sütunu
        self.scrollable_frame.columnconfigure(2, weight=2)  # Artist sütunu

        for index, track in enumerate(tracks, start=1):
            # 1. Sütun: Sıra Numarası
            index_label = ttk.Label(self.scrollable_frame, text=str(index), width=3, anchor="e")
            index_label.grid(row=index, column=0, padx=(5, 10), pady=8, sticky="e")

            # 2. Sütun: Şarkı Adı
            title_label = ttk.Label(self.scrollable_frame, text=track.title, anchor="w")
            title_label.grid(row=index, column=1, padx=5, pady=8, sticky="we")

            # 3. Sütun: Sanatçı Adı
            artist_label = ttk.Label(self.scrollable_frame, text=track.artist, anchor="w")
            artist_label.grid(row=index, column=2, padx=5, pady=8, sticky="we")

            # 4. Sütun: Listen Butonu (En sağa yapışık olacak)
            listen_button = self.create_listen_button(track.url)
            listen_button.grid(row=index, column=3, padx=15, pady=8, sticky="e")

            self.track_buttons.append(listen_button)

    def create_listen_button(self, track_url: str) -> ttk.Button:
        return ttk.Button(
            self.scrollable_frame,
            text="Listen",
            command=lambda: BrowserUtils.open_track_url(track_url)
        )
