# YT Video Factory

Automated YouTube video creation pipeline. Clone any channel's style, generate videos, and upload them as private drafts — all on autopilot.

Works with **Claude Code**, **Gemini CLI**, **Cursor**, or any AI coding agent.

## What It Does

1. **Scrapes** a YouTube channel's top videos and extracts their "viral DNA" (hooks, rhythm, structure)
2. **Generates** scripts in that channel's style about YOUR topics
3. **Creates** cinematic images for each slide (Gathos API)
4. **Generates** voiceover narration (Gathos TTS)
5. **Assembles** everything into a 1920x1080 video with FFmpeg
6. **Auto-generates** a YouTube thumbnail
7. **Uploads** to YouTube as a private draft (Zernio API — optional)

---

## Quick Setup (5 minutes)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/yt-video-factory.git
cd yt-video-factory
```

### 2. Install system dependencies

```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install yt-dlp ffmpeg

# Windows (via winget)
winget install yt-dlp.yt-dlp Gyan.FFmpeg
# Or via pip + manual FFmpeg download:
pip install yt-dlp
# Download FFmpeg from https://ffmpeg.org/download.html and add to PATH
```

### 3. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Set up API keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
# Required — get both at https://gathos.com
GATHOS_IMAGE_API_KEY=img_live_your_key_here
GATHOS_TTS_API_KEY=tts_live_your_key_here

# Optional — for auto YouTube upload
# Sign up at https://zernio.com, connect your YouTube channel, then paste key
ZERNIO_API_KEY=your_key_here
```

### 5. Verify setup

```bash
PYTHONPATH=. python3 pipeline.py --check
```

You should see all green checkmarks.

---

## Mode 1: Channel Clone (Claude Code Loop)

**Best for:** Continuously generating videos in another channel's style.

### What you provide:
| Input | Example |
|-------|---------|
| YouTube channel URL | `https://youtube.com/@clearvaluetax9382` |
| Topics (list) | "inflation tips, gold investing, tax strategies" |
| Voice | `josh` (preset) or any custom cloned voice name |
| Image style | `documentary` (or text-heavy, 3d-render, sketch, anime) |
| Video duration | `120` (seconds) |

### How to run:

**Step 1:** Open Claude Code (or your AI agent) in the `yt-video-factory` directory:

```bash
cd yt-video-factory
claude
```

**Step 2:** Tell the agent what to do:

```
Clone this channel: https://youtube.com/@clearvaluetax9382

Topics:
- Why inflation is eating your savings
- How to protect your money in 2026
- The truth about the US dollar

Voice: josh
Style: documentary
Duration: 120 seconds

Keep going until all topics are done.
```

**Step 3:** The agent handles everything automatically:
- Scrapes top 20 popular videos from the channel
- Transcribes them via yt-dlp subtitles
- Extracts viral DNA (hook patterns, sentence rhythm, retention loops)
- For each topic: generates script → images → voiceover → assembles video → uploads as YouTube draft
- Loops through all topics, one video at a time

**Step 4:** Check your YouTube Studio — videos appear as private drafts. Review title/description, then publish.

### Running as a continuous loop:

You can also use Claude Code's `/loop` command:

```
/loop Clone channel https://youtube.com/@clearvaluetax9382, voice josh, style documentary, 120s videos. Topics: inflation, gold, taxes, housing market, stock market. One video per loop.
```

---

## Mode 2: Script Folder (Obsidian / Markdown)

**Best for:** When you already have narration scripts written (in Obsidian, Notion exports, or any `.md` files).

### What you provide:
| Input | Example |
|-------|---------|
| Folder path | `/Users/me/Obsidian/video-scripts/` |
| Voice | `koko` |
| Image style | `text-heavy` |

### Script file format:

Just plain narration text in a `.md` file. No special format needed.

```markdown
# Why Gold Is the Ultimate Safe Haven

Right now, gold is hitting record highs. And most people
still don't understand why. Let me show you exactly what's
happening and why it matters for your money...
```

The title comes from the `# heading` or the filename.

### How to run:

**Step 1:** Open Claude Code in the `yt-video-factory` directory.

**Step 2:** Tell the agent:

```
Process all scripts from /Users/me/Obsidian/video-scripts/
Voice: koko
Style: text-heavy
```

**Step 3:** The agent reads each `.md` file, breaks it into slides, generates images + voiceover, assembles the video, and uploads. One video at a time, skipping already-processed scripts.

---

## Image Styles

| Style | What it looks like | Text in image? |
|-------|-------------------|----------------|
| `documentary` | Photorealistic cinematic photography | No |
| `text-heavy` | Bold graphics with text baked into images | Yes |
| `3d-render` | Stylized 3D scenes with volumetric lighting | No |
| `sketch` | Hand-drawn illustration style | No |
| `anime` | Anime/manga art style | No |

## Available Voices

### Preset Voices
| Voice | Style |
|-------|-------|
| `josh` | Professional, general narration |
| `koko` | Warm, conversational |
| `pixxy` | Energetic, youthful |
| `prof` | Academic, authoritative |
| `rochie` | Deep, dramatic |
| `spraky` | Casual, friendly |

### Custom Voice Cloning
You can clone your own voice on [gathos.com](https://gathos.com) and use it by name. Just provide your custom voice name instead of a preset (e.g., `voice: my-voice-name`).

---

## Output

Each video produces:

```
outputs/<timestamp>_<title>/
├── slides.json      # Slide definitions
├── slides/          # Generated images (1344x768)
├── audio/           # Voiceover WAV files
├── thumbnail.png    # YouTube thumbnail (1280x720)
└── final.mp4        # Final video (1920x1080, H.264)
```

Run state tracked in `state/<run_id>.json` — pipeline is resumable if interrupted.

---

## YouTube Upload (Optional)

To auto-upload videos as private drafts:

1. Sign up at [zernio.com](https://zernio.com)
2. Connect your YouTube channel (Zernio handles the Google OAuth)
3. Copy your API key from the dashboard
4. Add to `.env`: `ZERNIO_API_KEY=your_key`

Videos upload as **private** — you review in YouTube Studio and publish when ready.

Without Zernio, the pipeline still works — videos save locally.

---

## API Keys Summary

| Service | Key format | What it does | Required? |
|---------|-----------|-------------|-----------|
| [Gathos](https://gathos.com) | `img_live_*` | Image generation | Yes |
| [Gathos](https://gathos.com) | `tts_live_*` | Text-to-speech voiceover | Yes |
| [Zernio](https://zernio.com) | API key | YouTube upload as draft | Optional |

---

## CLI Reference

```bash
# Check all dependencies
PYTHONPATH=. python3 pipeline.py --check

# Create a new run
PYTHONPATH=. python3 pipeline.py --create --title "My Video" --style documentary --voice josh

# Run all stages
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --run-all

# Run individual stages
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage images
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage tts
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage assembly
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage thumbnail
PYTHONPATH=. python3 pipeline.py --run-id <run_id> --stage upload

# List all runs
PYTHONPATH=. python3 pipeline.py --list
```

---

## License

MIT
