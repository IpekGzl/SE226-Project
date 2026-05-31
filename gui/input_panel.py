
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from config import GENRES, ERAS

BG_DARK   = "#0d0d0d"
BG_CARD   = "#181818"
ACCENT    = "#1db954"
TEXT_SEC  = "#b3b3b3"
BORDER    = "#282828"
FONT_MAIN = ("Helvetica", 10)
FONT_SM   = ("Helvetica", 9)


class InputPanel:
    """Left-side control panel: mood input, genre/era/count selectors, generate button."""

    def __init__(self, parent: ttk.Frame, on_generate: Callable):
        self._on_generate_cb = on_generate

        frame = ttk.Frame(parent, style="TFrame", padding=(20, 16, 12, 16))
        frame.pack(side="left", fill="y", ipadx=4)
        frame.pack_propagate(False)
        frame.configure(width=340)

        self._build(frame)

    @property
    def gen_btn(self) -> ttk.Button:
        return self._gen_btn

    @property
    def status_var(self) -> tk.StringVar:
        return self._status_var

    def _build(self, frame: ttk.Frame):
        ttk.Label(frame, text="Your Mood (English or Turkish)",
                  style="Accent.TLabel").pack(anchor="w")
        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=(2, 6))

        self._journal_text = tk.Text(
            frame, height=7, wrap="word",
            bg=BG_CARD, fg="#ffffff",
            insertbackground=ACCENT,
            relief="flat", font=FONT_MAIN,
            padx=8, pady=8,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            highlightthickness=1,
        )
        self._journal_text.pack(fill="x")
        self._journal_text.insert("1.0",
            "I was looking at the sea in İzmir. It was raining softly, "
            "and an old song was playing through my headphones. "
            "I felt both peaceful and melancholic...")

        pad = {"pady": (12, 0)}

        ttk.Label(frame, text="Genre", style="Accent.TLabel").pack(anchor="w", **pad)
        self._genre_var = tk.StringVar(value=GENRES[0])
        ttk.Combobox(frame, textvariable=self._genre_var,
                     values=GENRES, state="readonly").pack(fill="x", pady=(4, 0))

        ttk.Label(frame, text="Era", style="Accent.TLabel").pack(anchor="w", **pad)
        self._era_var = tk.StringVar(value="2000s")
        ttk.Combobox(frame, textvariable=self._era_var,
                     values=ERAS, state="readonly").pack(fill="x", pady=(4, 0))

        ttk.Label(frame, text="Track Count", style="Accent.TLabel").pack(anchor="w", **pad)
        self._track_count_var = tk.IntVar(value=10)
        ttk.Spinbox(frame, from_=6, to=14,
                    textvariable=self._track_count_var,
                    state="readonly", width=6).pack(anchor="w", pady=(4, 0))

        self._gen_btn = ttk.Button(frame, text="GENERATE ALBUM",
                                   style="Accent.TButton", command=self._on_click)
        self._gen_btn.pack(fill="x", pady=(18, 0))

        self._status_var = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self._status_var,
                  style="Dim.TLabel", wraplength=300).pack(anchor="w", pady=(8, 0))

    def _on_click(self):
        journal = self._journal_text.get("1.0", "end").strip()
        if not journal:
            messagebox.showwarning("Missing Input", "Please enter a mood or journal text.")
            return
        self._on_generate_cb(
            journal,
            self._genre_var.get(),
            self._era_var.get(),
            self._track_count_var.get(),
        )
