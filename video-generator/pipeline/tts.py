"""Stage 2: scene narration text -> audio file + word-level timestamps.
"""
import wave
from google import genai
import os
import base64
from .models import SceneAudio
from .config import config


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

    # Calculate duration in seconds directly from the PCM byte array
    bytes_per_sample = channels * sample_width
    total_samples = len(pcm) // bytes_per_sample
    duration = total_samples / rate

    return duration


def synthesize_scene(scene_index: int, text: str, out_dir: str) -> SceneAudio:
    client = genai.Client(api_key=config.gemini_api_key)

    interaction = client.interactions.create(
        model="gemini-3.1-flash-tts-preview",
        input=f"Say narratingly: {text}!",
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": "Fenrir"}
            ]
        }
    )

    audio_path = os.path.join(out_dir, f"scene_{scene_index}.wav")
    duration: float = wave_file(
        audio_path, base64.b64decode(interaction.output_audio.data))

    return SceneAudio(
        scene_index=scene_index,
        audio_path=audio_path,
        duration=duration
    )
