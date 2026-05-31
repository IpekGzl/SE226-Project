
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import webbrowser
import json
import os
from PIL import Image, ImageTk

from config import GENRES, ERAS
from gemini_api import generate_album_metadata
from lastfm_api import build_tracklist
from image_gen import generate_cover_image
from input_panel import InputPanel
from status_manager import StatusManager

BG_DARK   = "#0d0d0d"
BG_CARD   = "#181818"
BG_ROW    = "#1e1e1e"
ACCENT    = "#1db954"
ACCENT_DK = "#158a3e"
TEXT_PRI  = "#ffffff"
TEXT_SEC  = "#b3b3b3"
TEXT_DIM  = "#535353"
BORDER    = "#282828"
FONT_MAIN = ("Helvetica", 10)
FONT_SM   = ("Helvetica", 9)
FONT_H1   = ("Helvetica", 22, "bold")
FONT_H2   = ("Helvetica", 13, "bold")


class AlbumCoverStudio:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Album Cover Studio")
        self.root.configure(bg=BG_DARK)
        self.root.geometry("1050x750")
        self.root.minsize(900, 650)

        self._cover_image = None
        self._cover_photo = None
        self._album_data = None
        self._tracklist = []

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=BG_DARK, foreground=TEXT_PRI,
                        fieldbackground=BG_CARD, font=FONT_MAIN)
        style.configure("TFrame", background=BG_DARK)
        style.configure("Card.TFrame", background=BG_CARD)
        style.configure("Row.TFrame", background=BG_ROW)
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRI, font=FONT_MAIN)
        style.configure("Dim.TLabel", background=BG_DARK, foreground=TEXT_SEC, font=FONT_SM)
        style.configure("Card.TLabel", background=BG_CARD, foreground=TEXT_PRI, font=FONT_MAIN)
        style.configure("CardDim.TLabel", background=BG_CARD, foreground=TEXT_SEC, font=FONT_SM)
        style.configure("Row.TLabel", background=BG_ROW, foreground=TEXT_PRI, font=FONT_MAIN)
        style.configure("RowDim.TLabel", background=BG_ROW, foreground=TEXT_SEC, font=FONT_SM)
        style.configure("Accent.TLabel", background=BG_DARK, foreground=ACCENT,
                        font=("Helvetica", 9, "bold"))
        style.configure("H1.TLabel", background=BG_DARK, foreground=TEXT_PRI, font=FONT_H1)
        style.configure("H2.TLabel", background=BG_CARD, foreground=TEXT_PRI, font=FONT_H2)
        style.configure("Tag.TLabel", background=BG_CARD, foreground=ACCENT, font=("Helvetica", 9))
        style.configure("Accent.TButton", background=ACCENT, foreground="#000000",
                        font=("Helvetica", 10, "bold"), borderwidth=0, relief="flat", padding=(12, 8))
        style.map("Accent.TButton", background=[("active", ACCENT_DK), ("pressed", ACCENT_DK)])
        style.configure("Listen.TButton", background="#333333", foreground=TEXT_PRI,
                        font=("Helvetica", 8, "bold"), borderwidth=0, relief="flat", padding=(6, 4))
        style.map("Listen.TButton",
                  background=[("active", ACCENT), ("pressed", ACCENT_DK)],
                  foreground=[("active", "#000000")])
        style.configure("Save.TButton", background=ACCENT, foreground="#000000",
                        font=("Helvetica", 10, "bold"), borderwidth=0, relief="flat", padding=(10, 7))
        style.map("Save.TButton", background=[("active", ACCENT_DK)])
        style.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD,
                        foreground=TEXT_PRI, selectbackground=BG_CARD,
                        selectforeground=TEXT_PRI, arrowcolor=ACCENT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", BG_CARD)],
                  foreground=[("readonly", TEXT_PRI)])
        style.configure("TSpinbox", fieldbackground=BG_CARD, background=BG_CARD,
                        foreground=TEXT_PRI, arrowcolor=ACCENT)

    def _build_ui(self):
        hdr = ttk.Frame(self.root, style="TFrame", padding=(20, 14, 20, 10))
        hdr.pack(fill="x")
        ttk.Label(hdr, text="Album Cover Studio", style="H1.TLabel").pack(side="left")
        ttk.Label(hdr, text="Describe your mood, enjoy the generated tracklist.",
                  style="Dim.TLabel").pack(side="left", padx=(14, 0))
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        body = ttk.Frame(self.root, style="TFrame")
        body.pack(fill="both", expand=True)

        self._input_panel = InputPanel(body, on_generate=self._on_generate)
        self._status_manager = StatusManager(self._input_panel.status_var,
                                             self._input_panel.gen_btn)
        self._right_panel(body)

    def _right_panel(self, parent):
        outer = ttk.Frame(parent, style="TFrame", padding=(8, 8, 16, 16))
        outer.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG_DARK, highlightthickness=0)
        vbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._result_frame = ttk.Frame(canvas, style="TFrame")
        self._canvas_window = canvas.create_window((0, 0), window=self._result_frame, anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(self._canvas_window, width=e.width))
        self._result_frame.bind("<Configure>",
                                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self._show_placeholder()

    def _show_placeholder(self):
        for w in self._result_frame.winfo_children():
            w.destroy()
        ph = ttk.Frame(self._result_frame, style="TFrame", padding=60)
        ph.pack(expand=True, fill="both")
        ttk.Label(ph, text="🎵", font=("Helvetica", 48),
                  background=BG_DARK, foreground=TEXT_DIM).pack()
        ttk.Label(ph, text="Generated tracklist will be shown here.",
                  style="Dim.TLabel").pack(pady=(10, 0))

    def _on_generate(self, journal, genre, era, track_count):
        self._status_manager.set_generating()
        self._show_placeholder()
        threading.Thread(
            target=self._generate_worker,
            args=(journal, genre, era, track_count),
            daemon=True
        ).start()

    def _generate_worker(self, journal, genre, era, track_count):
        try:
            self._status_manager.set_status("🤖 Gemini is thinking...")
            album_data = generate_album_metadata(journal, genre, era, track_count)

            self._status_manager.set_status("🎵 Fetching tracks from Last.fm...")
            tags = album_data.get("lastfm_tags", [])
            tracklist = build_tracklist(tags, track_count)
            if not tracklist:
                tracklist = build_tracklist([genre.lower()], track_count)
            album_data["tracklist"] = tracklist

            self._status_manager.set_status("🎨 Generating cover art...")
            cover_img = generate_cover_image(album_data.get("cover_prompt", "abstract album cover"))

            self._cover_image = cover_img
            self._album_data = album_data
            self._tracklist = tracklist
            self.root.after(0, self._show_album)

        except Exception as exc:
            err_msg = str(exc)
            self.root.after(0, lambda: self._on_error(err_msg))

    def _on_error(self, msg):
        self._status_manager.set_error(msg)
        messagebox.showerror("Generation Failed", msg)

    def _show_album(self):
        for w in self._result_frame.winfo_children():
            w.destroy()

        data = self._album_data
        tracks = self._tracklist

        header_card = ttk.Frame(self._result_frame, style="Card.TFrame", padding=16)
        header_card.pack(fill="x", padx=2, pady=(4, 0))

        img_resized = self._cover_image.resize((130, 130), Image.LANCZOS)
        self._cover_photo = ImageTk.PhotoImage(img_resized)
        tk.Label(header_card, image=self._cover_photo, bg=BG_CARD, bd=0).pack(side="left", anchor="n")

        meta = ttk.Frame(header_card, style="Card.TFrame", padding=(14, 0, 0, 0))
        meta.pack(side="left", fill="both", expand=True)

        ttk.Label(meta, text="ALBUM · CURATED PLAYLIST",
                  style="CardDim.TLabel", font=("Helvetica", 8, "bold")).pack(anchor="w")
        ttk.Label(meta, text=data.get("album_name", "Unknown Album"),
                  style="H2.TLabel", font=("Helvetica", 20, "bold")).pack(anchor="w", pady=(2, 4))
        ttk.Label(meta, text=data.get("mood_description", ""),
                  style="CardDim.TLabel", wraplength=420, justify="left").pack(anchor="w")
        ttk.Label(meta,
                  text=f"{data.get('year','')}  •  {len(tracks)} songs  •  {data.get('label','')}",
                  style="CardDim.TLabel").pack(anchor="w", pady=(6, 4))
        ttk.Label(meta, text="  ".join(f"#{t}" for t in data.get("lastfm_tags", [])[:6]),
                  style="Tag.TLabel").pack(anchor="w")
        ttk.Label(meta,
                  text="⚠ Album name, artist & label are AI-generated fiction. Songs are real (Last.fm).",
                  style="CardDim.TLabel", font=("Helvetica", 8)).pack(anchor="w", pady=(8, 0))

        tk.Frame(self._result_frame, bg=BORDER, height=1).pack(fill="x", padx=2, pady=6)
        col_hdr = ttk.Frame(self._result_frame, style="Card.TFrame", padding=(12, 4, 12, 4))
        col_hdr.pack(fill="x", padx=2)
        ttk.Label(col_hdr, text="#", style="CardDim.TLabel", width=3).pack(side="left")
        ttk.Label(col_hdr, text="TITLE", style="CardDim.TLabel",
                  font=("Helvetica", 8, "bold")).pack(side="left", padx=(8, 0), expand=True, anchor="w")
        tk.Frame(self._result_frame, bg=BORDER, height=1).pack(fill="x", padx=2, pady=(2, 0))

        for i, track in enumerate(tracks, 1):
            self._track_row(i, track)

        tk.Frame(self._result_frame, bg=BORDER, height=1).pack(fill="x", padx=2, pady=(8, 0))
        ttk.Button(self._result_frame, text="💾  SAVE ALBUM (JSON + PNG)",
                   style="Save.TButton", command=self._save_album).pack(fill="x", padx=2, pady=(6, 12))

        self._status_manager.set_done(len(tracks))

    def _track_row(self, index, track):
        row = ttk.Frame(self._result_frame, style="Row.TFrame", padding=(12, 6, 12, 6))
        row.pack(fill="x", padx=2)

        ttk.Label(row, text=str(index), style="RowDim.TLabel", width=3, anchor="e").pack(side="left")

        info = ttk.Frame(row, style="Row.TFrame")
        info.pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Label(info, text=track["title"], style="Row.TLabel",
                  font=("Helvetica", 10, "bold")).pack(anchor="w")
        ttk.Label(info, text=track["artist"], style="RowDim.TLabel").pack(anchor="w")

        if track.get("url"):
            ttk.Button(row, text="LISTEN", style="Listen.TButton",
                       command=lambda u=track["url"]: webbrowser.open(u)).pack(side="right")

    def _save_album(self):
        if not self._album_data or not self._cover_image:
            messagebox.showwarning("Nothing to Save", "Generate an album first.")
            return
        folder = filedialog.askdirectory(title="Choose Save Folder")
        if not folder:
            return
        name = self._album_data.get("album_name", "album").replace(" ", "_")
        json_path = os.path.join(folder, f"{name}.json")
        png_path  = os.path.join(folder, f"{name}_cover.png")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self._album_data, f, ensure_ascii=False, indent=2)
        self._cover_image.save(png_path, "PNG")
        messagebox.showinfo("Saved!", f"Kaydedildi:\n{json_path}\n{png_path}")
