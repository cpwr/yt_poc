import logging
import multiprocessing
import os

API_KEY = os.getenv("YT_SECRET_KEY")

from yt_dlp import DownloadError, YoutubeDL

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)

DIRECTORY = os.path.dirname(__file__)
DOWNLOAD_DIR = f"{DIRECTORY}/downloads"


def download_subtitles(video_data):
    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["all"],
        "subtitlesformat": "srv3",
        "outtmpl": f"{DOWNLOAD_DIR}/%(id)s",
        "skip_download": True,
        "quiet": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_data["url"])
    except DownloadError:
        logging.error("❌ DonwloadError")
        return


def extract_video_data(url):
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url=url, download=False)
        try:
            video_info = video_info["entries"]
        except KeyError:
            video_info["url"] = video_info["original_url"]
            download_subtitles(video_info)
        else:
            with multiprocessing.Pool() as process:
                process.map(download_subtitles, video_info)


if __name__ == "__main__":
    extract_video_data("https://www.youtube.com/watch?v=J9YnwUdJ3Z8")
