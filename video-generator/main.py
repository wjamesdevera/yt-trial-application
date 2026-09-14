"""End-to-end orchestration: topic -> raw mp4.

Usage:
    python main.py "why octopuses are so intelligent"
"""
import os
import sys
import uuid

from pipeline.config import config
from pipeline.script_gen import generate_script
from pipeline.tts import synthesize_scene
from pipeline.sourcing import fetch_asset
from pipeline.music import pick_track
from pipeline.assemble import render_scene, concat_scenes, mix_music


def run(topic: str) -> str:

    run_id = uuid.uuid4().hex[:8]
    work_dir = os.path.join(config.work_dir, run_id)
    os.makedirs(work_dir, exist_ok=True)
    print(f"[1/5] Working directory: {work_dir}")

    # 1. Script
    print("[2/5] Generating script with Gemini...")
    script = generate_script(topic)
    for i, scene in enumerate(script.scenes):
        print(f"   scene {i}: {scene.media_type:5s} | {scene.visual_query!r}")

    rendered_scenes = []

    for i, scene in enumerate(script.scenes):
        print(f"[3/5] Scene {i}: synthesizing voice...")
        audio = synthesize_scene(i, scene.narration, work_dir)

        print(
            f"[4/5] Scene {i}: sourcing visual asset ('{scene.visual_query}')...")
        asset = fetch_asset(
            scene, i, min_duration=audio.duration, out_dir=work_dir)

        rendered = render_scene(asset, audio, work_dir)
        rendered_scenes.append(rendered)

    print("[5/5] Concatenating scenes and mixing music...")
    concat_path = concat_scenes(rendered_scenes, work_dir)

    music_path = pick_track("default")
    final_path = os.path.join(work_dir, "final.mp4")
    mix_music(concat_path, music_path, final_path)

    print(f"\nDone. Final video: {final_path}")
    return final_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<topic>\"")
        sys.exit(1)
    run(sys.argv[1])
