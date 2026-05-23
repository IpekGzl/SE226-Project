from typing import Optional
from PIL import Image

from models.album_model import AlbumModel
from models.track_model import TrackModel


class AppState:

    def __init__(self) -> None:

        self.album: Optional[AlbumModel] = None

        self.tracks: list[TrackModel] = []

        self.cover_image: Optional[Image.Image] = None

    def reset(self) -> None:

        self.album = None

        self.tracks.clear()

        self.cover_image = None
