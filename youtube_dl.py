from dataclasses import dataclass, field
from datetime import datetime
import os
from pathlib import Path
from pytz import timezone
from yt_dlp import YoutubeDL


@dataclass
class dl_data:
    format_count: int = 0
    format_now: int = 1


dd = dl_data()


def youtube_dl(
    url,
    format="movie",
    quality="Best",
    ext=None,
    title="%(title)s",
    storage="Downloads",
    overwrite=True,
    timestamp="Now",
    progress_hooks=None,
):
    if not ext:
        if format != "audio":
            ext = "mp4"
        else:
            ext = "mp3"

    format_dict = {
        "movie": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "movie_mute": "bestvideo[ext=mp4]",
        "audio": "bestaudio",
    }

    if isinstance(quality, int):
        format_dict["movie"] = f"bestvideo[height<={quality}]+bestaudio[ext=m4a]"
        format_dict["movie_mute"] = f"bestvideo[height<={quality}]"

    ydl_opts = {
        "outtmpl": os.path.join(storage, f"{title}.%(ext)s"),
        "format": format_dict[format],
    }

    dd.format_count = 0

    if progress_hooks:
        ydl_opts["progress_hooks"] = progress_hooks

    if format == "audio":
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": ext,
            }
        ]

    if overwrite:
        ydl_opts["overwrites"] = True

    if "instagram.com" in url:
        ydl_opts["cookiefile"] = "instagram_cookie.txt"

    dd.format_now = 1
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        file_path = Path(ydl.prepare_filename(result))

    file_path = file_path.with_suffix(f".{ext}")
    absolute_path = file_path.resolve()

    if timestamp == "Now" and os.path.exists(absolute_path):
        now = datetime.now(timezone("Asia/Tokyo")).timestamp()
        os.utime(absolute_path, (now, now))

    return absolute_path
