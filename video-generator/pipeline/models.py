"""Shared data models for the video generation pipeline."""
from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class Scene(BaseModel):
    narration: str = Field(
        ..., description="Voiceover line for this scene (1-2 sentences)."
    )
    visual_query: str = Field(
        ..., description="Concrete, stock-footage-searchable noun phrase."
    )
    media_type: Literal["video", "image"] = Field(
        ..., description="'video' if motion helps, else 'image'."
    )


class ScriptScenes(BaseModel):
    scenes: List[Scene]


class WordTiming(BaseModel):
    word: str
    start: float  # seconds
    end: float    # seconds


class SceneAudio(BaseModel):
    scene_index: int
    audio_path: str
    duration: float
    # word_timings: List[WordTiming]


class SceneAsset(BaseModel):
    scene_index: int
    media_type: Literal["video", "image"]
    file_path: str
    source_duration: Optional[float] = None  # None for images


class RenderedScene(BaseModel):
    scene_index: int
    video_path: str  # final per-scene mp4 (visual + captions, no music)
    duration: float
