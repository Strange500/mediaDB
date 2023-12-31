from os.path import isfile
import requests as r
import bs4



from mediaDB.extension.Indexers.common import IndexerCommon
from mediaDB.common import *
from mediaDB.settings import *
from mediaDB.exceptions import *


class Yggtorrent_manipulator():
    # CONST
        __DATE = datetime.now().strftime("%m_%d_%Y")
        NAME = "YggTorrent"
        CONFIG_EXEMPLE_URL = "https://raw.githubusercontent.com/Strange500/mediaDB/main/exemples/YggTorrent"
        SETTING_FILE = os.path.join(IndexerCommon.SETTING_DIRECTORY, NAME)
        VAR_DIRECTORY = os.path.join(IndexerCommon.VAR_DIRECTORY, NAME)
        CACHE_DIRECTORY = os.path.join(VAR_DIRECTORY, "cache")
        CACHE_DB_TV_FILE = os.path.join(CACHE_DIRECTORY, "DB_tv.json")
        CACHE_DB_MOVIE_FILE = os.path.join(CACHE_DIRECTORY, "DB_movie.json")
        media_types = [1, 3]

        # CREATE NEEDED FILES & DIRECTORY
        os.makedirs(VAR_DIRECTORY, exist_ok=True)
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
                # Download TMDB config file if not created
        if not isfile(SETTING_FILE) and not wget(CONFIG_EXEMPLE_URL, SETTING_FILE):
            raise ProviderConfigError
        if not isfile(CACHE_DB_TV_FILE) :
            with open(CACHE_DB_TV_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)
        if not isfile(CACHE_DB_MOVIE_FILE) :
            with open(CACHE_DB_MOVIE_FILE, "w", encoding="utf-8") as f:
                dump({}, f, indent=5)
        # SETTING UP 
        CONFIG = parseConfig(SETTING_FILE)
        if not IndexerCommon.checkConfig(CONFIG, {"api_key": 1, "timeout": 1}):
            raise ProviderConfigError
        API_KEY = CONFIG["api_key"]
        API_KEY = API_KEY[0]
        REQUESTS_TIMEOUT = int(CONFIG["timeout"][0])
        bar(0.001)
            # Download tmdb ids file
        if not isfile(GENRE_MOVIE_FILE):
            movie_list = tmdb.Genres().movie_list()
            with open(GENRE_MOVIE_FILE, "w") as f:
                save_json(f, movie_list)
        bar(0.03)
        if not isfile(GENRE_TV_FILE):
            tv_list = tmdb.Genres().tv_list()
            with open(GENRE_TV_FILE, "w") as f:
                save_json(f, tv_list)
        bar(0.03)
        with open(GENRE_MOVIE_FILE, "r") as f:
            MOVIE_GENRE_IDS = load(f)
        with open(GENRE_TV_FILE, "r") as f:
            TV_GENRE_IDS = load(f)
        bar(0.001)
            # update ids files
        if not isfile(IDS_MOVIE_FILE) :

            if wget(IDS_MOVIES_URL, IDS_MOVIE_FILE+".gz"):
                gzExtract(IDS_MOVIE_FILE+".gz", IDS_MOVIE_FILE) 
                makeIdsFile(IDS_MOVIE_FILE)
        bar(0.59)
        if not isfile(IDS_TV_FILE) :
            if wget(IDS_TV_URL, IDS_TV_FILE+".gz"):
                gzExtract(IDS_TV_FILE+".gz", IDS_TV_FILE)    
                makeIdsFile(IDS_TV_FILE)
        bar(0.2)
            # loads ids
        with open(IDS_MOVIE_FILE, "r", encoding="utf-8") as f:
            IDS_MOVIE = load(f)
        bar(0.05)
        with open(IDS_TV_FILE, "r", encoding="utf-8") as f:
            IDS_TV = load(f)
        bar(0.009)
            # loads DB
        with open(CACHE_DB_TV_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_TV = load(f)
        with open(CACHE_DB_MOVIE_FILE, "r", encoding="utf-8") as f:
            CACHE_DB_MOVIE = load(f)
        bar(1.)
