
# controllers/worker_controller.py

import threading
from typing import Callable
import tkinter as tk

class WorkerController:
    def __init__(self, app_root: tk.Tk):
        self.root = app_root

    def start_generation_thread(self, generation_callback: Callable) -> None:
        """İş mantığını arka planda (thread) başlatarak GUI donmasını engeller."""
        thread = threading.Thread(target=generation_callback, daemon=True)
        thread.start()

    def safe_ui_callback(self, callback: Callable, *args) -> None:
        """Tkinter ana iş parçacığı (main thread) üzerinde güvenli bir şekilde UI günceller."""
        self.root.after(0, lambda: callback(*args))
