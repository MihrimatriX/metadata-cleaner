import os
import shutil
from typing import Optional

from mutagen import File as MutagenFile

from logs.logger import logger


def remove_audio_metadata(file_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Remove metadata from audio files using Mutagen (MP3, FLAC, Ogg, MP4/M4A, etc.).

    If output_path is set, the input is copied there first and only the copy is modified.
      If output_path is None, tags are stripped in place.
    """
    try:
        target = file_path
        if output_path:
            shutil.copy2(file_path, output_path)
            target = output_path

        audio = MutagenFile(target)
        if audio is None:
            logger.error(f"Could not read audio file (unsupported or corrupt): {target}")
            if output_path and os.path.isfile(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass
            return None

        audio.delete()
        audio.save()
        return target

    except Exception as e:
        logger.error(f"Error removing metadata from {file_path}: {e}", exc_info=True)
        if output_path and os.path.isfile(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass
        return None
