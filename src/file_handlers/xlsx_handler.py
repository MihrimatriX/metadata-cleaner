import os
from typing import Any, Optional

import openpyxl

from logs.logger import logger


def _blank_props(props: Any) -> None:
    """Clear common workbook core properties (openpyxl uses camelCase for some fields)."""
    for name in (
        "title",
        "subject",
        "description",
        "keywords",
        "category",
        "creator",
        "lastModifiedBy",
    ):
        if hasattr(props, name):
            setattr(props, name, "")


def remove_xlsx_metadata(file_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """Remove workbook metadata from an XLSX file."""
    try:
        wb = openpyxl.load_workbook(file_path)
        _blank_props(wb.properties)

        if not output_path:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_cleaned{ext}"

        wb.save(output_path)
        return output_path

    except Exception as e:
        logger.error(f"Error removing metadata from XLSX {file_path}: {e}", exc_info=True)
        return None
