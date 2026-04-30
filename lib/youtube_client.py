import os
import requests
from pathlib import Path
from lib.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN

TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
UPLOAD_ENDPOINT = "https://www.googleapis.com/upload/youtube/v3/videos"
THUMBNAIL_ENDPOINT = "https://www.googleapis.com/youtube/v3/thumbnails/set"


def get_access_token() -> str:
    resp = requests.post(TOKEN_ENDPOINT, data={
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "refresh_token": YOUTUBE_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()["access_token"]


def upload_video(
    file_path: str,
    title: str,
    description: str,
    tags: list[str] = None,
    thumbnail_path: str = "",
    visibility: str = "private",
    category_id: str = "22",
) -> dict:
    """Upload a video directly to YouTube using the Data API v3."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": visibility,
            "selfDeclaredMadeForKids": False,
        },
    }

    print("  Initiating resumable upload...")
    init_resp = requests.post(
        f"{UPLOAD_ENDPOINT}?uploadType=resumable&part=snippet,status",
        headers={**headers, "Content-Type": "application/json"},
        json=metadata,
        timeout=30,
    )
    init_resp.raise_for_status()
    upload_url = init_resp.headers["Location"]

    file_size = os.path.getsize(file_path)
    print(f"  Uploading video ({file_size / 1024 / 1024:.1f} MB)...")

    with open(file_path, "rb") as f:
        upload_resp = requests.put(
            upload_url,
            headers={
                **headers,
                "Content-Type": "video/*",
                "Content-Length": str(file_size),
            },
            data=f,
            timeout=600,
        )
    upload_resp.raise_for_status()
    result = upload_resp.json()
    video_id = result["id"]
    print(f"  Video uploaded: https://youtube.com/watch?v={video_id}")

    if thumbnail_path and Path(thumbnail_path).exists():
        print("  Uploading thumbnail...")
        try:
            with open(thumbnail_path, "rb") as f:
                thumb_resp = requests.post(
                    f"{THUMBNAIL_ENDPOINT}?videoId={video_id}",
                    headers={**headers, "Content-Type": "image/png"},
                    data=f,
                    timeout=60,
                )
            thumb_resp.raise_for_status()
            print("  Thumbnail set successfully")
        except Exception as e:
            print(f"  Thumbnail upload failed (video still uploaded): {e}")

    return {
        "video_id": video_id,
        "url": f"https://youtube.com/watch?v={video_id}",
        "title": title,
        "visibility": visibility,
        "method": "youtube_direct",
    }
