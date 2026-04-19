# YT Video Factory — Agent Guide

An end-to-end pipeline that creates YouTube videos and uploads them as private drafts. Works with any AI agent (Claude Code, Gemini CLI, Cursor, etc.).

## Two Modes

### Mode 1: Channel Clone (Loop Mode)
The agent analyzes a YouTube channel, extracts its "viral DNA" (style, hooks, rhythm — NOT topics), then continuously generates new videos in that style about user-provided topics.

### Mode 2: Script Folder (Obsidian Mode)
The agent watches a folder of narration scripts and processes each one into a video.

---

## Prerequisites

```bash
# Install system dependencies
brew install yt-dlp ffmpeg  # macOS
# or: apt install yt-dlp ffmpeg  # Linux

# Install Python dependencies
cd yt-video-factory
pip3 install -r requirements.txt

# Copy .env and fill in your API keys
cp .env.example .env
```

### Required API Keys
| Key | Service | Get it at |
|-----|---------|-----------|
| `GATHOS_IMAGE_API_KEY` | Image generation (`img_live_*`) | https://gathos.com |
| `GATHOS_TTS_API_KEY` | Text-to-speech (`tts_live_*`) | https://gathos.com |
| `ZERNIO_API_KEY` | YouTube upload | https://zernio.com |

### Zernio Setup (for YouTube upload)
Before the pipeline can upload videos to YouTube, the user must:
1. Sign up at [zernio.com](https://zernio.com)
2. Connect their YouTube channel — Zernio walks you through Google OAuth
3. Copy the API key from the Zernio dashboard
4. Paste it into `.env` as `ZERNIO_API_KEY`

Without this, the pipeline still works end-to-end — it just saves the video and thumbnail locally instead of uploading.

### Check everything works
```bash
PYTHONPATH=. python3 pipeline.py --check
```

---

## Mode 1: Channel Clone (Loop Mode)

### What the User Provides
1. **YouTube channel URL** — the channel to clone the style from
2. **Topics** — a list of topics to create videos about (the agent picks one per iteration)
3. **Voice** — a preset (josh, koko, pixxy, prof, rochie, spraky) or a custom cloned voice name from Gathos (stays the same for all videos)
4. **Image style** — one of: text-heavy, documentary, 3d-render, sketch, anime
5. **Video duration** — target length in seconds (e.g., 60, 120, 180). Used to calculate word count:
   - 60s = ~150 words
   - 120s = ~300 words
   - 180s = ~450 words
   - Formula: `duration × 2.5 = total words`

### Important: What Viral DNA IS and ISN'T
- **IS**: The channel's hook patterns, sentence rhythm, retention loops, content structure, tone, and pacing
- **ISN'T**: The channel's topics — topics come from the USER, not the DNA
- The DNA teaches HOW to write, not WHAT to write about

### Step-by-Step Loop

#### STEP 1: Analyze Channel (One-time setup)

Scrape the top 20 most popular videos (sorted by view count) and transcribe them:

```bash
PYTHONPATH=. python3 -c "
from lib.channel_analyzer import get_channel_transcripts
import json
transcripts = get_channel_transcripts('CHANNEL_URL', 20)
with open('outputs/channel_dna_raw.json', 'w') as f:
    json.dump(transcripts, f, indent=2)
print(f'Got {len(transcripts)} transcripts')
"
```

Then read `outputs/channel_dna_raw.json` and follow the instructions in `skills/viral-dna-extractor.md` to extract viral DNA. Save the result as `outputs/viral_dna.md`.

This only runs ONCE per channel. Reuse `viral_dna.md` for all subsequent videos.

#### STEP 2: Generate Script (Each iteration)

Pick the next topic from the user's topic list. Using the viral DNA from `outputs/viral_dna.md`, generate a narration script that:
- Follows the hook architecture, retention loops, and sentence rhythm from the DNA
- Is about the user's specified topic (NOT the source channel's topic)
- Hits the target word count based on requested duration (`duration × 2.5 words`)
- Is pure narration text — no stage directions, no timecodes, no [brackets]

#### STEP 3: Create Slides JSON

Read the skill at `skills/script-to-slides.md` and follow its instructions to convert the script into `slides.json`.

1. First create the run:
```bash
PYTHONPATH=. python3 pipeline.py --create --title "YOUR VIDEO TITLE" --style documentary --voice josh --mode channel --channel-url "CHANNEL_URL"
```

2. Note the `run_id` and `output_dir` from the output.

3. Write `slides.json` to the run's output directory:
```bash
cat > outputs/<run_id>/slides.json << 'SLIDES_EOF'
{
  "title": "...",
  "description": "...",
  ...the full slides JSON...
}
SLIDES_EOF
```

#### STEP 4: Run Pipeline

```bash
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --run-all
```

This executes: images → TTS → assembly → thumbnail → YouTube upload (as private draft).

If `ZERNIO_API_KEY` is not set, the upload stage will be skipped — the video and thumbnail are still saved locally.

#### STEP 5: Report & Loop

Report to the user:
- Video title
- Path to final.mp4
- Path to thumbnail.png
- YouTube upload status (private draft, or skipped if no Zernio key)

Then go back to STEP 2, pick the next topic, and generate the next video. One video at a time. Keep going until the user stops the loop or all topics are exhausted.

---

## Mode 2: Script Folder (Obsidian Mode)

### What the User Provides
1. **Folder path** — path to an Obsidian (or any) folder containing `.md` script files
2. **Voice** — one of: josh, koko, pixxy, prof, rochie, spraky
3. **Image style** — one of: text-heavy, documentary, 3d-render, sketch, anime

### Script File Format
Scripts are plain narration text in `.md` files. No special format required — just the words to be spoken. The agent handles breaking them into slides.

Optionally, the file can start with a `# Title` heading which becomes the video title. Otherwise, the title is derived from the filename.

### Step-by-Step Loop

#### STEP 1: Scan Folder

List all `.md` files in the provided folder:
```bash
ls -1 "FOLDER_PATH"/*.md
```

Check which ones have already been processed by looking at existing runs:
```bash
PYTHONPATH=. python3 pipeline.py --list
```

Pick the first unprocessed `.md` file.

#### STEP 2: Read Script

Read the `.md` file. The content is pure narration text. Extract the title from either:
- The first heading in the file (if it starts with `#`)
- The filename (e.g., `why-ai-will-replace-jobs.md` → "Why AI Will Replace Jobs")

#### STEP 3: Create Slides JSON

Follow `skills/script-to-slides.md` to convert the narration into `slides.json`.

1. Create the run:
```bash
PYTHONPATH=. python3 pipeline.py --create --title "EXTRACTED TITLE" --style documentary --voice josh --mode folder
```

2. Write `slides.json` to the run directory.

#### STEP 4: Run Pipeline

```bash
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --run-all
```

#### STEP 5: Report & Loop

Report results, then go back to STEP 1 to check for the next unprocessed script. One video at a time.

---

## Duration Guide

| Requested Duration | Word Count | Approx Slides (3-4s each) |
|-------------------|------------|---------------------------|
| 30s (Short) | ~75 words | 5-8 slides |
| 60s | ~150 words | 10-15 slides |
| 90s | ~225 words | 15-20 slides |
| 120s (2 min) | ~300 words | 20-25 slides |
| 180s (3 min) | ~450 words | 30-40 slides |
| 300s (5 min) | ~750 words | 50-60 slides |

Formula: `words = duration_seconds × 2.5`

---

## Stage-by-Stage (Manual Control)

If you need to run stages individually (e.g., to retry a failed stage):

```bash
# Generate images only (skips existing files)
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage images

# Generate TTS only
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage tts

# Assemble video only (requires images + TTS)
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage assembly

# Generate thumbnail only
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage thumbnail

# Upload to YouTube only (requires assembled video + ZERNIO_API_KEY)
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage upload
```

---

## Output Structure

Each run creates:
```
outputs/<run_id>/
├── slides.json          # Slide definitions (created by agent)
├── slides/
│   ├── slide-01.png     # Generated images
│   ├── slide-02.png
│   └── ...
├── audio/
│   ├── slide-01.wav     # Generated voiceovers
│   ├── slide-02.wav
│   └── ...
├── thumbnail.png        # YouTube thumbnail
└── final.mp4            # Final assembled video (1920x1080, H.264)
```

State is tracked in:
```
state/<run_id>.json      # Stage progress, asset paths, status
```

---

## Image Styles Reference

| Style | Description | Text in image? | Prompt approach |
|-------|-------------|----------------|-----------------|
| `text-heavy` | Bold design system, text baked into images | Yes | Like idea-to-presentation: 5 hex colors, text placement, typography |
| `documentary` | Photorealistic cinematic shots | No | Clean, atmospheric, cinematic photography |
| `3d-render` | Stylized 3D renders with volumetric lighting | No | 3D scenes with dramatic lighting |
| `sketch` | Hand-drawn illustration style | No | Detailed pencil/ink drawings |
| `anime` | Anime/manga art style | No | High-quality anime illustrations |

### Text-Heavy Mode Details
When the user picks `text-heavy`, the agent must:
1. Create a 5-color design system (background, primary, secondary, accent, text hex codes)
2. Reference every hex by value in prompts (e.g., `"#E94560"` not `"primary"`)
3. Describe exact text content and placement in each image prompt
4. Include `on_screen_text` field in slides.json with headline/subtitle/body
5. Maintain visual continuity with consistent colors across all slides

---

## Available Voices

### Preset Voices
| Voice | Best for |
|-------|----------|
| `josh` | General, professional narration |
| `koko` | Warm, conversational |
| `pixxy` | Energetic, youthful |
| `prof` | Academic, authoritative |
| `rochie` | Deep, dramatic |
| `spraky` | Casual, friendly |

### Custom Cloned Voices
Users can clone their own voice on [gathos.com](https://gathos.com) and use it by name. Just provide the custom voice name instead of a preset — the pipeline passes it directly to the Gathos TTS API.

Example: if the user cloned their voice and named it `"brian"`, they just say `voice: brian` and it works.

The user picks a voice ONCE and it stays the same for all videos in the session.

---

## Troubleshooting

**yt-dlp fails to get transcripts**: Some videos don't have auto-captions. The pipeline skips those and moves on. Popular videos almost always have auto-captions.

**Gathos 502 errors**: Retry logic handles these automatically (up to 4 retries with backoff).

**Gathos API timeout**: Jobs timeout after 600 seconds. If it keeps timing out, the API may be under load — wait and retry.

**FFmpeg assembly fails**: Check that all slide images and audio files exist in the run directory.

**Zernio upload fails**: Make sure your YouTube account is connected at https://zernio.com and your API key has YouTube permissions.

**file.io upload fails**: The free tier has limits. Consider setting `FILE_HOST_URL` to your own storage endpoint.

**Image stage interrupted**: Rerunning `--stage images` skips already-generated images and only creates missing ones.
