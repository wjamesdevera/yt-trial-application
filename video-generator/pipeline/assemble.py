"""Stage 6: assemble per-scene visuals + audio + captions into a final mp4.

Approach: render each scene independently (visual trimmed/looped to the
narration's duration, captions burned in, voice audio attached), then
concat all scenes, then mix in ducked background music as a final pass.
"""
import os
import subprocess
from typing import List
from .models import SceneAsset, SceneAudio, RenderedScene
from .config import config


def _run(cmd: List[str]):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg command failed:\n{' '.join(cmd)}\n\nstderr:\n{result.stderr}")
    return result


def render_scene(asset: SceneAsset, audio: SceneAudio, out_dir: str) -> RenderedScene:
    """Combine one scene's visual + voice audio  mp4."""
    duration = audio.duration
    out_path = os.path.join(out_dir, f"scene_{asset.scene_index}_rendered.mp4")
    w, h = config.video_width, config.video_height

    # subtitles filter needs an escaped path on some platforms; keep paths simple/relative where possible

    if asset.media_type == "video":
        # Loop the source clip if it's shorter than the narration, then trim to exact duration.
        vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", asset.file_path,
            "-i", audio.audio_path,
            "-t", str(duration),
            "-vf", vf,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest",
            out_path,
        ]
    else:
        # Image: apply a slow Ken Burns zoom/pan over the scene duration.
        fps = config.fps
        zoom_frames = int(duration * fps)
        vf = (
            f"scale={w*2}:{h*2},"
            f"zoompan=z='min(zoom+0.0008,1.15)':d={zoom_frames}:s={w}x{h}:fps={fps},"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", asset.file_path,
            "-i", audio.audio_path,
            "-t", str(duration),
            "-vf", vf,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest",
            out_path,
        ]

    _run(cmd)
    return RenderedScene(scene_index=asset.scene_index, video_path=out_path, duration=duration)


def concat_scenes(rendered_scenes: List[RenderedScene], out_dir: str) -> str:
    """Concatenate rendered scene clips in order into one video (voice audio intact)."""
    filelist_path = os.path.join(out_dir, "filelist.txt")
    with open(filelist_path, "w") as f:
        for scene in sorted(rendered_scenes, key=lambda s: s.scene_index):
            f.write(f"file '{os.path.abspath(scene.video_path)}'\n")

    concat_out = os.path.join(out_dir, "concat_novid_music.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", filelist_path,
        "-c:v", "libx264", "-c:a", "aac",
        concat_out,
    ]
    _run(cmd)
    return concat_out


def mix_music(video_with_voice: str, music_path: str, out_path: str, music_volume: float = 0.15) -> str:
    """Overlay background music under the existing voice track, looping/trimming music to video length."""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_with_voice,
        "-stream_loop", "-1", "-i", music_path,
        "-filter_complex",
        f"[1:a]volume={music_volume}[music_low];"
        f"[0:a][music_low]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac",
        "-shortest",
        out_path,
    ]
    _run(cmd)
    return out_path
