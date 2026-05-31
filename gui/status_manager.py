
import tkinter as tk
from tkinter import ttk


class StatusManager:
    """Controls the status label text and the generate button's enabled/disabled state."""

    def __init__(self, status_var: tk.StringVar, gen_btn: ttk.Button):
        self._status_var = status_var
        self._gen_btn = gen_btn

    def set_status(self, message: str):
        self._status_var.set(message)

    def set_generating(self):
        self._gen_btn.state(["disabled"])
        self._status_var.set("⏳ Starting generation...")

    def set_done(self, track_count: int):
        self._status_var.set(f"✅ {track_count} real songs loaded.")
        self._gen_btn.state(["!disabled"])

    def set_error(self, message: str):
        self._status_var.set(f"❌ Error: {message}")
        self._gen_btn.state(["!disabled"])
