import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from gui.track_table import TrackTable


class AlbumPanel(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.cover_label = None
        self.album_title = None
        self.artist_label = None
        self.year_label = None

        self.track_table = None

        self.cover_image_ref = None

        self.setup_ui()

    def setup_ui(self):

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=15, pady=15)

        self.cover_label = ttk.Label(top_frame)
        self.cover_label.pack(side=tk.LEFT, padx=10)

        info_frame = ttk.Frame(top_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.album_title = ttk.Label(
            info_frame,
            text="Album Title",
            font=("Arial", 20, "bold")
        )

        self.album_title.pack(anchor="w")

        self.artist_label = ttk.Label(
            info_frame,
            text="Artist"
        )

        self.artist_label.pack(anchor="w")

        self.year_label = ttk.Label(
            info_frame,
            text="Year"
        )

        self.year_label.pack(anchor="w")

        self.track_table = TrackTable(self)

        self.track_table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=10
        )

    def update_album(
        self,
        album_data,
        tracks,
        image
    ) -> None:

        resized = image.resize((250, 250))

        photo = ImageTk.PhotoImage(resized)

        self.cover_label.configure(image=photo)

        self.cover_image_ref = photo

        self.album_title.configure(
            text=album_data.album_name
        )

        self.artist_label.configure(
            text=album_data.artist_name
        )

        self.year_label.configure(
            text=album_data.year
        )

        self.track_table.render_tracks(tracks)
