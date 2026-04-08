import os
import concurrent.futures
from typing import List, Optional, Set

from tqdm import tqdm

from logs.logger import logger
from file_handlers.image_handler import remove_image_metadata
from file_handlers.pdf_handler import remove_pdf_metadata
from file_handlers.docx_handler import remove_docx_metadata
from file_handlers.audio_handler import remove_audio_metadata
from file_handlers.video_handler import remove_video_metadata
from file_handlers.xlsx_handler import remove_xlsx_metadata
from file_handlers.pptx_handler import remove_pptx_metadata

# Mapping of supported file extensions to their corresponding removal functions
SUPPORTED_EXTENSIONS = {
    ".jpg": remove_image_metadata,
    ".jpeg": remove_image_metadata,
    ".png": remove_image_metadata,
    ".bmp": remove_image_metadata,
    ".tiff": remove_image_metadata,
    ".webp": remove_image_metadata,
    ".heic": remove_image_metadata,
    ".pdf": remove_pdf_metadata,
    ".docx": remove_docx_metadata,
    ".mp3": remove_audio_metadata,
    ".wav": remove_audio_metadata,
    ".flac": remove_audio_metadata,
    ".ogg": remove_audio_metadata,
    ".m4a": remove_audio_metadata,
    ".mp4": remove_video_metadata,
    ".mkv": remove_video_metadata,
    ".mov": remove_video_metadata,
    ".avi": remove_video_metadata,
    ".xlsx": remove_xlsx_metadata,
    ".pptx": remove_pptx_metadata,
}

IMAGE_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".heic"}

def remove_metadata(file_path: str, output_path: Optional[str] = None, config_file: Optional[str] = None) -> Optional[str]:
    """
    Remove metadata from a single file.

    Parameters:
        file_path (str): Path to the file to be processed.
        output_path (Optional[str]): Custom output path. If None, a default naming scheme is used.
        config_file (Optional[str]): Path to a JSON configuration file for selective metadata filtering.

    Returns:
        Optional[str]: The path to the cleaned file if successful, else None.
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            logger.warning(f"Unsupported file type: {ext}")
            raise ValueError(f"Unsupported file type: {ext}")

        logger.info(f"Processing file: {file_path}")
        remover_function = SUPPORTED_EXTENSIONS[ext]

        if ext in IMAGE_EXTENSIONS:
            cleaned_file = remover_function(file_path, output_path, config_file)
        else:
            cleaned_file = remover_function(file_path, output_path)

        if cleaned_file and os.path.exists(cleaned_file):
            logger.info(f"Metadata removed successfully: {cleaned_file}")
            return cleaned_file
        else:
            logger.error(f"Failed to process file: {file_path}")
            return None

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
        return None

def _output_path_for_folder_job(
    file_path: str, folder_path: str, output_folder: str, recursive: bool
) -> str:
    if recursive:
        rel = os.path.relpath(os.path.abspath(file_path), os.path.abspath(folder_path))
        if rel.startswith(".."):
            rel = os.path.basename(file_path)
    else:
        rel = os.path.basename(file_path)
    return os.path.normpath(os.path.join(output_folder, rel))


def _is_under_path(entry: str, ancestor: str) -> bool:
    entry = os.path.normpath(os.path.abspath(entry))
    ancestor = os.path.normpath(os.path.abspath(ancestor))
    if entry == ancestor:
        return True
    prefix = ancestor.rstrip(os.sep) + os.sep
    return entry.startswith(prefix)


def _skip_because_inside_output_only(
    file_path: str, batch_root: str, output_folder_abs: str
) -> bool:
    """Skip files already sitting under the output tree (e.g. previous cleaned/)."""
    root_abs = os.path.normpath(os.path.abspath(batch_root))
    out_abs = os.path.normpath(os.path.abspath(output_folder_abs))
    if out_abs == root_abs:
        return False
    fp_abs = os.path.normpath(os.path.abspath(file_path))
    return _is_under_path(fp_abs, out_abs)


def process_file(
    file_path: str,
    folder_path: str,
    output_folder: str,
    recursive: bool,
    config_file: Optional[str] = None,
) -> Optional[str]:
    """
    Process a single file and remove its metadata (used by folder batch / worker pool).

    Parameters:
        file_path (str): Path to the file.
        folder_path (str): Root folder of the batch (used for relative output paths when recursive).
        output_folder (str): Folder tree where cleaned files are written.
        recursive (bool): If True, preserve subfolder structure under output_folder.
        config_file (Optional[str]): Configuration file for metadata filtering (for images).

    Returns:
        Optional[str]: The path to the cleaned file if successful, else None.
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            logger.warning(f"⚠️ Unsupported file type: {file_path}")
            return None

        output_path = _output_path_for_folder_job(file_path, folder_path, output_folder, recursive)
        dest_dir = os.path.dirname(output_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)

        if ext in IMAGE_EXTENSIONS:
            cleaned_file = SUPPORTED_EXTENSIONS[ext](file_path, output_path, config_file)
        else:
            cleaned_file = SUPPORTED_EXTENSIONS[ext](file_path, output_path)

        if cleaned_file and os.path.exists(cleaned_file):
            logger.info(f"✅ Metadata removed: {cleaned_file}")
            return cleaned_file

        logger.error(f"❌ Failed to process: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}", exc_info=True)
        return None

def remove_metadata_from_folder(folder_path: str,
                                  output_folder: Optional[str] = None,
                                  config_file: Optional[str] = None,
                                  recursive: bool = False) -> List[str]:
    """
    Remove metadata from all supported files within a folder.

    Parameters:
        folder_path (str): Path to the folder containing files.
        output_folder (Optional[str]): Folder to save cleaned files. If None, a 'cleaned' subfolder is created.
        config_file (Optional[str]): Configuration file for selective metadata filtering (applied to images).
        recursive (bool): If True, process files in subfolders recursively.

    Returns:
        List[str]: A list of paths to successfully cleaned files.
    """
    if not os.path.exists(folder_path):
        logger.error(f"❌ Folder not found: {folder_path}")
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not output_folder:
        output_folder = os.path.join(folder_path, "cleaned")
    os.makedirs(output_folder, exist_ok=True)
    output_folder_abs = os.path.normpath(os.path.abspath(output_folder))

    files_to_process: List[str] = []
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if _skip_because_inside_output_only(file_path, folder_path, output_folder_abs):
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    files_to_process.append(file_path)
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if _skip_because_inside_output_only(file_path, folder_path, output_folder_abs):
                continue
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    files_to_process.append(file_path)

    processed_files: List[str] = []
    failed_files: List[str] = []

    max_workers = min(32, (os.cpu_count() or 4) * 2)
    with tqdm(total=len(files_to_process), desc="Processing Files", unit="file") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    process_file, fp, folder_path, output_folder, recursive, config_file
                ): fp
                for fp in files_to_process
            }

            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                if result:
                    processed_files.append(result)
                else:
                    failed_files.append(future_to_file[future])
                pbar.update(1)

    logger.info("\n📊 Summary Report:")
    logger.info(f"✅ Successfully processed: {len(processed_files)} files")
    logger.info(f"❌ Failed to process: {len(failed_files)} files")
    if failed_files:
        logger.info("⚠️ Failed Files:")
        for file in failed_files:
            logger.info(f"  - {file}")

    return processed_files
