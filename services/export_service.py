import json
import os
from datetime import datetime
from tkinter import filedialog

from PIL import Image


class ExportService:

    def choose_export_directory(self) -> str:

        folder = filedialog.askdirectory(
            title="Choose Export Folder"
        )

        return folder

    def export_album_json(
        self,
        album_data: dict,
        output_dir: str
    ) -> str:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_path = os.path.join(
            output_dir,
            f"album_{timestamp}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                album_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return file_path

    def export_cover_png(
        self,
        image: Image.Image,
        output_dir: str
    ) -> str:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_path = os.path.join(
            output_dir,
            f"cover_{timestamp}.png"
        )

        image.save(file_path, "PNG")

        return file_path
