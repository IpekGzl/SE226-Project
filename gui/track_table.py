import tkinter as tk
from tkinter import ttk

from utils.browser_utils import BrowserUtils


class TrackTable(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.track_buttons = []

        self.setup_ui()

    def setup_ui(self):

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

    def render_tracks(
        self,
        tracks
    ) -> None:

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.track_buttons.clear()

        for index, track in enumerate(tracks, start=1):

            row = ttk.Frame(self.scrollable_frame)

            row.pack(
                fill=tk.X,
                padx=5,
                pady=5
            )

            index_label = ttk.Label(
                row,
                text=str(index),
                width=5
            )

            index_label.pack(side=tk.LEFT)

            title_label = ttk.Label(
                row,
                text=track.title,
                width=35
            )

            title_label.pack(side=tk.LEFT)

            artist_label = ttk.Label(
                row,
                text=track.artist,
                width=25
            )

            artist_label.pack(side=tk.LEFT)

            listen_button = self.create_listen_button(
                track.url
            )

            listen_button.pack(
                side=tk.RIGHT,
                padx=5
            )

            self.track_buttons.append(
                listen_button
            )

    def create_listen_button(
        self,
        track_url: str
    ) -> ttk.Button:

        button = ttk.Button(
            self.scrollable_frame,
            text="Listen",
            command=lambda: BrowserUtils.open_track_url(track_url)
        )

        return button
