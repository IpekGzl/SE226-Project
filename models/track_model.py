
class TrackModel:

    def __init__(self, title, artist, url):

        self.title = title
        self.artist = artist
        self.url = url

    def __str__(self):

        return self.title + " - " + self.artist
