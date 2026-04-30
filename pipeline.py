#!/usr/bin/env python3
"""
YT Video Factory — Pipeline Orchestrator

Usage (called by the AI agent, not directly by users):

    # Check dependencies
    python3 pipeline.py --check

    # Run individual stages for a run
    python3 pipeline.py --run-id <run_id> --stage images
    python3 pipeline.py --run-id <run_id> --stage tts
    python3 pipeline.py --run-id <run_id> --stage assembly
    python3 pipeline.py --run-id <run_id> --stage thumbnail
    python3 pipeline.py --run-id <run_id> --stage upload

    # Run all stages (images → tts → assembly → thumbnail → upload)
    python3 pipeline.py --run-id <run_id> --run-all

    # Create a new run (agent writes slides.json first, then calls this)
    python3 pipeline.py --create --title "Video Title" --style documentary --voice josh

    # List runs
    python3 pipeline.py --list
"""

import argparse
import json
import sys
from pathlib import Path

from lib.config import OUTPUTS_DIR, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT
from lib import state as run_state
from lib.gathos_client import generate_images_batch, generate_tts_batch, generate_thumbnail
from lib.video_assembler import assemble_video
from lib.media_host import upload_file


def check_dependencies():
    import shutil

    deps = {
        "yt-dlp": shutil.which("yt-dlp"),
        "ffmpeg": shutil.which("ffmpeg"),
        "ffprobe": shutil.which("ffprobe"),
    }

    all_ok = True
    for name, path in deps.items():
        if path:
            print(f"  ✓ {name}: {path}")
        else:
            print(f"  ✗ {name}: NOT FOUND")
            all_ok = False

    from lib.config import GATHOS_IMAGE_API_KEY, GATHOS_TTS_API_KEY

    if GATHOS_IMAGE_API_KEY:
        print(f"  ✓ GATHOS_IMAGE_API_KEY: set")
    else:
        print(f"  ✗ GATHOS_IMAGE_API_KEY: not set")
        all_ok = False

    if GATHOS_TTS_API_KEY:
        print(f"  ✓ GATHOS_TTS_API_KEY: set")
    else:
        print(f"  ✗ GATHOS_TTS_API_KEY: not set")
        all_ok = False

    from lib.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN

    yt_direct = all([YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN])
    if yt_direct:
        print(f"  ✓ YouTube Direct: configured (Client ID + Secret + Refresh Token)")
    else:
        print(f"  ⚠ YouTube Direct: not configured — videos will be saved locally only")

    return all_ok


def stage_images(run_id: str):
    """Generate all slide images via Gathos."""
    state = run_state.load_run(run_id)
    run_dir = state["output_dir"]
    slides_path = Path(run_dir) / "slides.json"

    if not slides_path.exists():
        raise FileNotFoundError(f"slides.json not found at {slides_path}. Agent must create it first.")

    slides_json = json.loads(slides_path.read_text())
    slides = slides_json["slides"]

    run_state.update_stage(run_id, "images", "in_progress")
    print(f"\n[IMAGES] Generating {len(slides)} slide images...")

    prompts = []
    for slide in slides:
        prompts.append({
            "prompt": slide["image_prompt"],
            "filename": f"slide-{slide['slide_number']:02d}.png",
        })

    slides_dir = str(Path(run_dir) / "slides")
    results = generate_images_batch(prompts, slides_dir)

    for i, path in enumerate(results):
        run_state.set_slide_asset(run_id, slides[i]["slide_number"], "image", path)

    run_state.update_stage(run_id, "images", "complete")
    print(f"[IMAGES] Done — {len(results)} images generated")
    return results


def stage_tts(run_id: str):
    """Generate voiceover audio for all slides via Gathos TTS."""
    state = run_state.load_run(run_id)
    run_dir = state["output_dir"]
    voice = state["voice"]
    slides_path = Path(run_dir) / "slides.json"

    slides_json = json.loads(slides_path.read_text())
    slides = slides_json["slides"]

    run_state.update_stage(run_id, "tts", "in_progress")
    print(f"\n[TTS] Generating {len(slides)} voiceovers with voice '{voice}'...")

    items = []
    for slide in slides:
        items.append({
            "text": slide["narration"],
            "filename": f"slide-{slide['slide_number']:02d}.wav",
        })

    audio_dir = str(Path(run_dir) / "audio")
    results = generate_tts_batch(items, audio_dir, voice)

    for i, path in enumerate(results):
        run_state.set_slide_asset(run_id, slides[i]["slide_number"], "audio", path)

    run_state.update_stage(run_id, "tts", "complete")
    print(f"[TTS] Done — {len(results)} audio files generated")
    return results


def stage_assembly(run_id: str):
    """Assemble final video from images + audio using FFmpeg."""
    state = run_state.load_run(run_id)
    run_dir = state["output_dir"]
    slides_path = Path(run_dir) / "slides.json"

    slides_json = json.loads(slides_path.read_text())

    run_state.update_stage(run_id, "assembly", "in_progress")
    print(f"\n[ASSEMBLY] Building final video...")

    final_path = assemble_video(run_dir, slides_json)

    run_state.update_stage(run_id, "assembly", "complete", final_path)
    run_state.update_run(run_id, {"status": "assembled"})
    print(f"[ASSEMBLY] Done — {final_path}")
    return final_path


def stage_thumbnail(run_id: str):
    """Generate thumbnail image via Gathos."""
    state = run_state.load_run(run_id)
    run_dir = state["output_dir"]
    slides_path = Path(run_dir) / "slides.json"

    slides_json = json.loads(slides_path.read_text())
    thumb_prompt = slides_json.get("thumbnail_prompt", "")

    if not thumb_prompt:
        print("[THUMBNAIL] No thumbnail_prompt in slides.json, skipping")
        run_state.update_stage(run_id, "thumbnail", "skipped")
        return None

    run_state.update_stage(run_id, "thumbnail", "in_progress")
    print(f"\n[THUMBNAIL] Generating thumbnail...")

    thumb_path = str(Path(run_dir) / "thumbnail.png")
    generate_thumbnail(thumb_prompt, thumb_path)

    run_state.update_stage(run_id, "thumbnail", "complete", thumb_path)
    print(f"[THUMBNAIL] Done — {thumb_path}")
    return thumb_path


def stage_upload(run_id: str):
    """Upload video + thumbnail to YouTube as private draft via YouTube Direct API."""
    from lib.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN

    use_youtube_direct = all([YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN])

    if not use_youtube_direct:
        print(f"\n[UPLOAD] Skipped — YouTube credentials not set. Video saved locally.")
        run_state.update_stage(run_id, "upload", "skipped")
        return None

    state = run_state.load_run(run_id)
    run_dir = state["output_dir"]
    slides_path = Path(run_dir) / "slides.json"

    slides_json = json.loads(slides_path.read_text())

    final_video = state["stages"]["assembly"].get("output", "")
    if not final_video or not Path(final_video).exists():
        raise FileNotFoundError("Final video not found. Run assembly stage first.")

    title = slides_json.get("title", state["title"])
    description = slides_json.get("description", "")
    tags = slides_json.get("tags", [])
    thumb_path = state["stages"]["thumbnail"].get("output", "")

    run_state.update_stage(run_id, "upload", "in_progress")

    from lib.youtube_client import upload_video as yt_direct_upload
    print(f"\n[UPLOAD] Uploading to YouTube directly (Google API)...")

    result = yt_direct_upload(
        file_path=final_video,
        title=title,
        description=description,
        tags=tags,
        thumbnail_path=thumb_path,
        visibility="private",
    )

    run_state.update_stage(run_id, "upload", "complete", json.dumps(result))
    run_state.update_run(run_id, {"status": "uploaded"})
    print(f"[UPLOAD] Done — video uploaded as private draft on YouTube")
    return result


def run_all(run_id: str):
    """Execute all stages in sequence."""
    state = run_state.load_run(run_id)
    print(f"\n{'='*60}")
    print(f"YT VIDEO FACTORY — Full Pipeline")
    print(f"Run: {run_id}")
    print(f"Title: {state['title']}")
    print(f"Style: {state['style']} | Voice: {state['voice']}")
    print(f"{'='*60}")

    run_state.update_run(run_id, {"status": "in_progress"})

    stage_images(run_id)
    stage_tts(run_id)
    stage_assembly(run_id)
    stage_thumbnail(run_id)
    stage_upload(run_id)

    run_state.update_run(run_id, {"status": "complete"})
    state = run_state.load_run(run_id)

    upload_status = state["stages"]["upload"].get("status", "unknown")
    yt_msg = "uploaded as private draft" if upload_status == "complete" else "skipped (no upload credentials)"

    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"  Video: {state['stages']['assembly'].get('output', '')}")
    print(f"  Thumbnail: {state['stages']['thumbnail'].get('output', 'skipped')}")
    print(f"  YouTube: {yt_msg}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="YT Video Factory Pipeline")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--create", action="store_true", help="Create a new run")
    parser.add_argument("--title", type=str, default="", help="Video title")
    parser.add_argument("--style", type=str, default="documentary", help="Image style")
    parser.add_argument("--voice", type=str, default="josh", help="TTS voice")
    parser.add_argument("--mode", type=str, default="manual", help="channel or folder or manual")
    parser.add_argument("--channel-url", type=str, default="", help="YouTube channel URL")
    parser.add_argument("--run-id", type=str, default="", help="Run ID to operate on")
    parser.add_argument("--stage", type=str, default="", help="Stage to run: images|tts|assembly|thumbnail|upload")
    parser.add_argument("--run-all", action="store_true", help="Run all stages")
    parser.add_argument("--list", action="store_true", help="List all runs")

    args = parser.parse_args()

    if args.check:
        ok = check_dependencies()
        sys.exit(0 if ok else 1)

    if args.list:
        runs = run_state.list_runs()
        if not runs:
            print("No runs found.")
        for r in runs:
            print(f"  {r['run_id']} — {r['status']} — {r['title']}")
        return

    if args.create:
        if not args.title:
            print("Error: --title required for --create")
            sys.exit(1)
        state = run_state.create_run(
            title=args.title,
            mode=args.mode,
            style=args.style,
            voice=args.voice,
            channel_url=args.channel_url,
        )
        print(f"Created run: {state['run_id']}")
        print(f"Output dir: {state['output_dir']}")
        print(json.dumps(state, indent=2))
        return

    if not args.run_id:
        print("Error: --run-id required")
        sys.exit(1)

    if args.run_all:
        run_all(args.run_id)
    elif args.stage:
        stage_map = {
            "images": stage_images,
            "tts": stage_tts,
            "assembly": stage_assembly,
            "thumbnail": stage_thumbnail,
            "upload": stage_upload,
        }
        if args.stage not in stage_map:
            print(f"Error: unknown stage '{args.stage}'. Options: {list(stage_map.keys())}")
            sys.exit(1)
        stage_map[args.stage](args.run_id)
    else:
        print("Error: specify --stage or --run-all")
        sys.exit(1)


if __name__ == "__main__":
    main()
