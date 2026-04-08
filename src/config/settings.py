import os
from typing import Dict, List

"""
Configuration settings for Metadata Cleaner.

These settings include default output directories, logging configurations, and 
supported file formats, grouped by file category.
"""

# Default output directory for cleaned files.
DEFAULT_OUTPUT_FOLDER: str = "cleaned"

# Flag to enable or disable parallel processing.
ENABLE_PARALLEL_PROCESSING: bool = True

# Logging configuration:
# LOG_FILE_PATH is the path where log files are saved.
# LOG_LEVEL sets the default logging level. Options: DEBUG, INFO, WARNING, ERROR.
LOG_FILE_PATH: str = os.path.join("src", "logs", "metadata_cleaner.log")
LOG_LEVEL: str = "INFO"

# Supported file formats, organized by file category.
SUPPORTED_FORMATS: Dict[str, List[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".tiff", ".webp", ".heic"],
    "documents": [".pdf", ".docx", ".xlsx", ".pptx"],
    "audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
    "videos": [".mp4", ".mkv", ".mov", ".avi"],
}
