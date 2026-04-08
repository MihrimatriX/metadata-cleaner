import os
import shutil
import subprocess
from typing import Optional

from logs.logger import logger


def _resolve_ffmpeg() -> Optional[str]:
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    bundled_win = os.path.join(root, "ffmpeg", "ffmpeg.exe")
    if os.path.isfile(bundled_win):
        return bundled_win
    bundled_unix = os.path.join(root, "ffmpeg", "ffmpeg")
    if os.path.isfile(bundled_unix):
        return bundled_unix
    return shutil.which("ffmpeg")


def remove_video_metadata(file_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Strip container metadata from a video file using FFmpeg (-map_metadata -1, stream copy).
    Requires ffmpeg on PATH or under project ffmpeg/.
    """
    ffmpeg_path = _resolve_ffmpeg()
    if not ffmpeg_path:
        logger.error("ffmpeg not found. Install ffmpeg or place ffmpeg/ffmpeg.exe next to the project.")
        return None
    try:
        if not output_path:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_cleaned{ext}"

        command = [
            ffmpeg_path,
            "-y",
            "-i",
            file_path,
            "-map_metadata",
            "-1",
            "-c",
            "copy",
            output_path,
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Error removing metadata from video {file_path}: {e}", exc_info=True)
        return None
