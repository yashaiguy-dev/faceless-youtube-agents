import os
import sys
import shutil
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

if sys.platform != "win32":
    _EXTRA_PATHS = ["/opt/homebrew/bin", "/usr/local/bin"]
    for _p in _EXTRA_PATHS:
        if _p not in os.environ.get("PATH", ""):
            os.environ["PATH"] = _p + os.pathsep + os.environ.get("PATH", "")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
STATE_DIR = BASE_DIR / "state"

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
ASPECT_RATIO = "16:9"
IMAGE_GEN_WIDTH = 1344
IMAGE_GEN_HEIGHT = 768
THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720

WORDS_PER_SECOND = 2.5
DEFAULT_SLIDE_DURATION = 4
MIN_SLIDE_DURATION = 3
MAX_SLIDE_DURATION = 10
DISSOLVE_DURATION = 0.5
FPS = 24

GATHOS_BASE_URL = "https://gathos.com/api/v1"
GATHOS_IMAGE_API_KEY = os.getenv("GATHOS_IMAGE_API_KEY", os.getenv("GATHOS_API_KEY", ""))
GATHOS_TTS_API_KEY = os.getenv("GATHOS_TTS_API_KEY", os.getenv("GATHOS_API_KEY", ""))
GATHOS_IMAGE_POLL_INTERVAL = 5
GATHOS_TTS_POLL_INTERVAL = 3
GATHOS_TIMEOUT = 600

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

FILE_HOST_URL = os.getenv("FILE_HOST_URL", "https://file.io")

PRESET_VOICES = ["josh", "koko", "pixxy", "prof", "rochie", "spraky"]
DEFAULT_VOICE = "josh"

IMAGE_STYLES = {
    "text-heavy": {
        "description": "Bold text baked into images with design system colors",
        "prompt_prefix": "A wide 16:9 bold modern flat illustration with text overlay.",
    },
    "presentation": {
        "description": "Structured presentation slides with headlines, bullets, stats, diagrams — uses two-stage design system engine",
        "prompt_prefix": "A wide 16:9 bold modern presentation slide.",
        "skill": "presentation-slides.md",
    },
    "documentary": {
        "description": "Clean photorealistic cinematic shots, no text",
        "prompt_prefix": "A wide 16:9 photorealistic cinematic photograph.",
    },
    "3d-render": {
        "description": "Stylized 3D renders, no text",
        "prompt_prefix": "A wide 16:9 high-quality 3D render with volumetric lighting.",
    },
    "sketch": {
        "description": "Hand-drawn sketch or whiteboard style, no text",
        "prompt_prefix": "A wide 16:9 detailed hand-drawn sketch illustration.",
    },
    "anime": {
        "description": "Anime/manga art style, no text",
        "prompt_prefix": "A wide 16:9 high-quality anime illustration.",
    },
    "infographic": {
        "description": "Data visualization with charts, statistics, comparisons, timelines — no text in prompt, agent adds data viz elements",
        "prompt_prefix": "A wide 16:9 clean modern infographic illustration with data visualization.",
    },
    "dark-tech": {
        "description": "Dark background with neon accents, clean typography — tech/productivity YouTube aesthetic",
        "prompt_prefix": "A wide 16:9 dark premium tech illustration. Near-black background with subtle glow effects and neon accent lighting.",
    },
    "whiteboard": {
        "description": "Hand-drawn whiteboard explainer style on white background — how-things-work channels",
        "prompt_prefix": "A wide 16:9 whiteboard explainer illustration. Clean white background with hand-drawn marker-style diagrams and annotations.",
    },
    "comic": {
        "description": "Comic book panel style with bold outlines and dramatic scenes — storytelling and drama channels",
        "prompt_prefix": "A wide 16:9 vivid comic book illustration with bold ink outlines and dramatic halftone shading.",
    },
    "stock": {
        "description": "Clean professional stock photography with subtle text overlays — business and corporate channels",
        "prompt_prefix": "A wide 16:9 high-quality professional stock photograph with clean composition and natural lighting.",
    },
}
DEFAULT_STYLE = "documentary"

YT_DLP_MAX_VIDEOS = 20
