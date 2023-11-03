class MediaNotFoundERROR(Exception):
    "Raise if an indexer can't find a media in it's database"

class MediaTypeNotSupported(Exception):
    "Raise if media type is not supported"

class MediaTypeDoesNotExist(Exception):
    "Raised if the media type is not initialsed"