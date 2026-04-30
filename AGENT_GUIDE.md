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

### YouTube Upload Setup (Optional)

Upload directly to YouTube using your own Google account. Free, no third-party service needed.

1. Follow the setup guide: `docs/YouTube-Direct-Upload-Setup.md`
2. You'll get 3 keys from Google Cloud Console + OAuth Playground (~15 min one-time setup)
3. Add them to `.env`:
```env
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REFRESH_TOKEN=your_refresh_token
```

Limit: ~6 uploads/day on free quota (can request more from Google).

Without these keys, the pipeline still works end-to-end — it just saves the video and thumbnail locally instead of uploading.

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
4. **Image style** — one of: presentation, text-heavy, dark-tech, infographic, whiteboard, documentary, 3d-render, sketch, anime, comic, stock
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

If YouTube credentials are not set, the upload stage will be skipped — the video and thumbnail are still saved locally.

#### STEP 5: Report & Loop

Report to the user:
- Video title
- Path to final.mp4
- Path to thumbnail.png
- YouTube upload status (private draft, or skipped if no YouTube credentials)

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

# Upload to YouTube only (requires assembled video + YouTube credentials)
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

### Text + Visual Styles (text baked into images)

| Style | Description | Best for |
|-------|-------------|----------|
| `presentation` | **Structured slides with headlines, bullets, stats, diagrams. Uses two-stage design system engine.** Read `skills/presentation-slides.md` for the full prompting approach. | Educational, how-to, listicles, tech explainers — **recommended for most faceless channels** |
| `text-heavy` | Bold flat design with text overlay and 5-color design system | Quick text-on-image videos, simple overlays |
| `dark-tech` | Dark background with neon accents, clean typography | Tech reviews, productivity, AI, programming |
| `infographic` | Data visualization with charts, statistics, comparisons, timelines | Finance, science, data-driven explainers |
| `whiteboard` | Hand-drawn marker-style on white background | How-things-work, education, process explainers |

### Visual-Only Styles (no text in images — narration carries the content)

| Style | Description | Best for |
|-------|-------------|----------|
| `documentary` | Photorealistic cinematic photography | News, finance, history, current events |
| `3d-render` | Stylized 3D with volumetric lighting | Tech, futuristic, science, gaming |
| `sketch` | Hand-drawn pencil/ink illustration | Storytelling, history, biographies |
| `anime` | Anime/manga art style | Entertainment, pop culture, gaming |
| `comic` | Comic book panels with bold outlines and halftone shading | Drama, storytelling, "what if" scenarios |
| `stock` | Clean professional stock photography | Business, corporate, career, self-improvement |

### Presentation Mode (RECOMMENDED)

When the user picks `presentation`, the agent MUST read `skills/presentation-slides.md` and follow its two-stage pipeline:

**Stage 1 — Design System:** Create a locked 5-color palette, 3 visual motifs, typography style, and mood BEFORE writing any slide prompts.

**Stage 2 — Rich Slide Prompts:** Each image prompt is 4-8 sentences with:
- Background treatment using exact hex codes (e.g., `"#0D1117"` not `"dark"`)
- All on-screen text with exact placement and styling
- Adaptive complexity (diagrams for educational, stat heroes for data, timelines for history)
- Visual continuity via recurring motifs and consistent design language

Each slide also gets a structured `on_screen_text` dict with keys like `headline`, `subtitle`, `bullet_points`, `stat`, `callout`, `diagram_labels`.

### Text-Heavy Mode

Simpler than presentation — use when you want quick text-on-image without the full two-stage pipeline:
1. Create a 5-color design system (background, primary, secondary, accent, text hex codes)
2. Reference every hex by value in prompts (e.g., `"#E94560"` not `"primary"`)
3. Describe exact text content and placement in each image prompt
4. Include `on_screen_text` field in slides.json with headline/subtitle/body
5. Maintain visual continuity with consistent colors across all slides

### Dark-Tech Mode

The trending YouTube aesthetic (Ali Abdaal, MKBHD, Fireship style):
1. Near-black background (`#0A0A0A` to `#1A1A2E`)
2. One or two neon accent colors (cyan, lime green, electric blue, magenta)
3. Clean sans-serif typography with wide letter-spacing
4. Subtle glow effects, gradients, and grid/circuit patterns
5. Minimal elements — lots of negative space
6. Text IS baked into images (headlines, stats, callouts)

### Infographic Mode

Data-driven visual approach:
1. Clean background (dark or light depending on topic mood)
2. Charts, graphs, and data visualizations as the main visual elements
3. Large stat numbers displayed prominently
4. Comparison layouts (vs., before/after, ranked lists)
5. Timelines for chronological content
6. Text IS baked into images (labels, values, axes)

### Whiteboard Mode

Classic explainer style:
1. Clean white or off-white background
2. Hand-drawn marker-style lines and shapes
3. Diagrams with arrows showing flow/process
4. Handwritten-style annotations and labels
5. Simple color palette (black lines + 2-3 marker colors)
6. Text IS baked into images (labels, annotations)

### Comic Mode

For storytelling and drama:
1. Bold black ink outlines on vivid colors
2. Dramatic angles, exaggerated expressions
3. Halftone dot shading and speed lines
4. Panel-style composition (single panel per slide)
5. NO speech bubbles (narration handles the dialogue)
6. High contrast, saturated colors

### Stock Mode

Professional and clean:
1. High-quality photography composition
2. Natural lighting, shallow depth of field
3. Clean subject isolation
4. Neutral color grading (warm or cool depending on topic)
5. NO text in image — visuals only
6. Business-appropriate imagery

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

**YouTube Direct upload fails**: Check that all 3 keys (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN) are in `.env`. If you get a 403, your refresh token may be revoked — re-do the OAuth Playground step. If you hit quota limits (~6/day), request a quota increase in Google Cloud Console.

**file.io upload fails**: The free tier has limits. Consider setting `FILE_HOST_URL` to your own storage endpoint if needed.

**Image stage interrupted**: Rerunning `--stage images` skips already-generated images and only creates missing ones.
