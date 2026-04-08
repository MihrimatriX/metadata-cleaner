import os
from typing import Optional

from pptx import Presentation

from logs.logger import logger


def remove_pptx_metadata(file_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """Clear core document properties from a PPTX file."""
    try:
        prs = Presentation(file_path)
        cp = prs.core_properties
        cp.author = ""
        cp.title = ""
        cp.subject = ""
        cp.keywords = ""
        cp.comments = ""
        cp.last_modified_by = ""

        if not output_path:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_cleaned{ext}"

        prs.save(output_path)
        return output_path

    except Exception as e:
        logger.error(f"Error removing metadata from PPTX {file_path}: {e}", exc_info=True)
        return None
