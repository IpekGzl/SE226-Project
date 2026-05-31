import io
from urllib.parse import quote
import requests
from PIL import Image

from config import (
    POLLINATIONS_BASE_URL,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    REQUEST_TIMEOUT
)


class ImageService:

    def build_cover_prompt(self, base_prompt: str, genre: str) -> str:
        genre_styles = {
            "Pop": "vibrant pop album cover, colorful lighting",
            "Rock": "dark rock aesthetic, dramatic shadows",
            "Hip-Hop / Rap": "urban hip hop style, cinematic",
            "Electronic": "futuristic electronic aesthetic, neon",
            "Indie": "indie film photography aesthetic",
            "R&B / Soul": "smooth soulful atmosphere",
            "Jazz": "vintage jazz club aesthetic",
            "Metal": "heavy metal dark fantasy aesthetic",
            "Türk Pop": "nostalgic turkish pop aesthetic",
            "Klasik": "classical orchestral elegant artwork"
        }

        style = genre_styles.get(genre, "modern album cover aesthetic")

        # ÇOK KRİTİK DÜZELTME: Satır sonu ve başı boşlukları temizlemek için tek satıra indirgiyoruz
        prompt_parts = [
            "album cover art",
            style,
            base_prompt.strip(),
            "highly detailed, professional music album artwork, square composition"
        ]

        # Parçaları virgülle birleştirip içindeki gereksiz ekstra boşlukları ve yeni satırları temizliyoruz
        final_prompt = ", ".join(prompt_parts)
        return " ".join(final_prompt.split())

    def generate_cover_image(self, prompt: str) -> Image.Image:
        encoded_prompt = quote(prompt)

        url = (
            f"{POLLINATIONS_BASE_URL}/{encoded_prompt}"
            f"?width={IMAGE_WIDTH}"
            f"&height={IMAGE_HEIGHT}"
            f"&nologo=true"
        )

        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        return image
