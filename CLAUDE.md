# YT Video Factory

## Project Instructions

When the user asks to create YouTube videos, run the video factory, clone a channel, or process scripts into videos:

1. Read `AGENT_GUIDE.md` for the full pipeline instructions
2. All Python commands must use `PYTHONPATH=/Users/psrmanju2/psr_workspace/yt-video-factory` and run from that directory
3. The `.env` file with API keys is at `yt-video-factory/.env`
4. Skills are in `skills/` — read them when needed for viral DNA extraction or script-to-slides conversion
5. Always use `pip3` and `python3` (never `pip` or `python`)
6. Use 10-minute timeouts for Gathos API jobs — never let a local timeout kill a running job

## Two Modes

### Channel Clone Mode
User says: "clone this channel" or "make videos like [channel URL]"
→ Follow Mode 1 in AGENT_GUIDE.md

### Script Folder Mode
User says: "process scripts from [folder]" or "make videos from my scripts"
→ Follow Mode 2 in AGENT_GUIDE.md

## Key Files
- `pipeline.py` — Main orchestrator (run stages via CLI)
- `lib/gathos_client.py` — Image + TTS generation
- `lib/channel_analyzer.py` — YouTube channel analysis
- `lib/video_assembler.py` — FFmpeg video assembly
- `lib/youtube_client.py` — YouTube Direct upload via Google API
- `lib/media_host.py` — File hosting for public URLs
- `skills/viral-dna-extractor.md` — How to extract viral DNA
- `skills/script-to-slides.md` — How to convert scripts to slides JSON
