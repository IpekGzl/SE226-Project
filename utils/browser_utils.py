import webbrowser


class BrowserUtils:

    @staticmethod
    def open_track_url(url: str) -> None:
        try:
            webbrowser.open(url)

        except Exception as e:
            print(f"Browser open error: {e}")
