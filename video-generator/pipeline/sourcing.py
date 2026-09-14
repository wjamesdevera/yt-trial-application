"""Stage 3: scene visual_query -> best-matching Pexels asset, downloaded locally.

Handles: orientation filtering, empty results, generic fallback query.
"""
import os
import requests
from typing import Optional
from .models import Scene, SceneAsset
from .config import config

PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"
PEXELS_PHOTO_SEARCH = "https://api.pexels.com/v1/search"

FALLBACK_QUERY = "abstract background texture"


def _headers():
    return {"Authorization": config.pexel_api_key}


def _is_vertical() -> bool:
    return config.video_height > config.video_width


def _search_videos(query: str, per_page: int = 5):
    resp = requests.get(
        PEXELS_VIDEO_SEARCH,
        headers=_headers(),
        params={"query": query, "per_page": per_page,
                "orientation": "portrait" if _is_vertical() else "landscape"},
    )
    resp.raise_for_status()
    return resp.json().get("videos", [])


def _search_photos(query: str, per_page: int = 5):
    resp = requests.get(
        PEXELS_PHOTO_SEARCH,
        headers=_headers(),
        params={"query": query, "per_page": per_page,
                "orientation": "portrait" if _is_vertical() else "landscape"},
    )
    resp.raise_for_status()
    return resp.json().get("photos", [])


def _pick_best_video_file(video: dict) -> Optional[dict]:
    """Pick the highest-resolution file under a reasonable size ceiling."""
    files = sorted(video.get("video_files", []),
                   key=lambda f: f.get("width", 0), reverse=True)
    for f in files:
        if f.get("width", 0) >= config.video_width * 0.5:  # avoid tiny/low-res renditions
            return f
    return files[0] if files else None


def _download(url: str, out_path: str) -> str:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return out_path


def fetch_asset(scene: Scene, scene_index: int, min_duration: float, out_dir: str) -> SceneAsset:
    query = scene.visual_query

    if scene.media_type == "video":
        results = _search_videos(query)
        if not results:
            # retry with a broader/simplified query before giving up
            simplified = " ".join(query.split()[:2])
            results = _search_videos(simplified)
        if not results:
            results = _search_videos(FALLBACK_QUERY)

        if results:
            # prefer clips at least as long as the narration; otherwise take the longest available
            candidates = sorted(results, key=lambda v: v.get(
                "duration", 0), reverse=True)
            best = next((v for v in candidates if v.get(
                "duration", 0) >= min_duration), candidates[0])
            file_info = _pick_best_video_file(best)
            out_path = os.path.join(out_dir, f"scene_{scene_index}_src.mp4")
            _download(file_info["link"], out_path)
            return SceneAsset(
                scene_index=scene_index,
                media_type="video",
                file_path=out_path,
                source_duration=best.get("duration"),
            )

    # image path (either media_type == "image" or video search totally failed)
    results = _search_photos(query) or _search_photos(FALLBACK_QUERY)
    best = results[0]
    img_url = best["src"]["original"]
    out_path = os.path.join(out_dir, f"scene_{scene_index}_src.jpg")
    _download(img_url, out_path)
    return SceneAsset(scene_index=scene_index, media_type="image", file_path=out_path, source_duration=None)
