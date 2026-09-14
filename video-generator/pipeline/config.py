from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "VideoGeneratorPipeline"
    gemini_api_key: str = ""
    pexel_api_key: str = ""

    # Script Settings
    gemini_model: str = "gemini-3.1-flash-lite"
    num_scenes: int = 6
    seconds_per_scene: int = 5

    # Video Settings
    video_width: int = 1080
    video_height: int = 1920  # vertical, change to 1920x1080 for horizontal
    fps: int = 30

    # Paths
    work_dir: str = "./work"        # scratch space, per-run subfolder created inside
    music_dir: str = "./assets/music"  # local royalty-free music library


config = Config()
