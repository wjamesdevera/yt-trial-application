from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

YDL_OPTS = {
    'quiet': True,
    'noplaylist': True,
    'skip_download': True,
    'extractor_args': {
        'youtube': ['player_client=android', 'player_skip=webpage']
    },
}


class ScrapeRequest(BaseModel):
    url: str


@app.post("/api/v1/videos/extract")
def read_root(request: ScrapeRequest):
    metadata = scrape(request.url)
    return metadata


def scrape(url: str) -> None:
    """Return basic metadata for a YouTube video."""

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)

    metadata = {
        "title": info.get("title"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "upload_date": info.get("upload_date"),
    }
    return metadata
