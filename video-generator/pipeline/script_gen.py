"""Stage 1: topic -> structured script (list of Scene) via Gemini."""
from google import genai
from .models import ScriptScenes
from .config import config

SCRIPT_PROMPT = """You are a scriptwriter for short-form video content (documentary-style explainer videos, similar to what you'd see on YouTube Shorts or TikTok).

Write a scene-by-scene script for a video about the following topic:

TOPIC: {topic}

Requirements for each scene:
- "narration": One to two sentences of spoken voiceover. Natural, conversational spoken language, not written prose. No stage directions, no speaker labels.
- "visual_query": A concrete, literal, physically-filmable noun phrase describing what should appear on screen during this narration. This will be used as a search query against a stock footage/photo library, so it must describe a literal visual scene, not an abstract idea.
    - BAD: "economic uncertainty", "the future of AI", "growing tensions"
    - GOOD: "stock market ticker board", "robotic arm assembling car parts", "two business people arguing across a table"
    - If the narration describes an abstract concept, translate it into a concrete visual metaphor or literal illustrative scene.
- "media_type": "video" if motion would help convey the scene (action, process, movement), "image" if a static photo is sufficient (portraits, objects, establishing shots, data/concepts).

Structure:
- Break the script into {num_scenes} scenes.
- Each scene's narration should be short enough to read aloud in roughly {seconds_per_scene} seconds.
- The script should have a clear hook in scene 1, build through the middle scenes, and end with a clear closing line in the last scene.

Output ONLY the structured data. Do not include any preamble, explanation, or markdown formatting.
"""


def generate_script(topic: str, num_scenes: int = None, seconds_per_scene: int = None) -> ScriptScenes:
    client = genai.Client(api_key=config.gemini_api_key)

    prompt = SCRIPT_PROMPT.format(
        topic=topic,
        num_scenes=num_scenes or config.num_scenes,
        seconds_per_scene=seconds_per_scene or config.seconds_per_scene,
    )

    response = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ScriptScenes.model_json_schema()
        },
    )

    return ScriptScenes.model_validate_json(response.output_text)
