"""Stage 5: pick a background music track.

Simplest workable approach: curate a small local library of royalty-free
tracks tagged by mood, and pick one by keyword match. Swap in Pixabay Music
API or similar if you want a larger catalog.
"""
import os
import random
from .config import config

# Map mood keyword -> filename in config.music_dir. Populate this yourself
# with tracks downloaded once from a royalty-free source (e.g. Pixabay Music,
# YouTube Audio Library) and confirmed for your intended use (commercial or not).
MOOD_LIBRARY = {
    "upbeat": ["upbeat_1.mp3", "upbeat_2.mp3"],
    "calm": ["calm_1.mp3", "calm_2.mp3"],
    "tense": ["tense_1.mp3"],
    "inspiring": ["inspiring_1.mp3"],
    "default": ["neutral_1.mp3"],
}


def pick_track(mood: str = "default") -> str:
    candidates = MOOD_LIBRARY.get(mood, MOOD_LIBRARY["default"])
    chosen = random.choice(candidates)
    path = os.path.join(config.music_dir, chosen)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Music file {path} not found. Populate {config.music_dir} "
            f"with tracks matching MOOD_LIBRARY filenames."
        )
    return path
