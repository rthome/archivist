import pathlib

import click
import exif

from typing import Iterable

RAW_EXTS = {".raf", ".nef", ".orf", ".rw2", ".crw", ".cr2", ".arw", ".dng"}
PROCESSED_EXTS = {".jpeg", ".jpg", ".heif", ".hif", ".heic"}
IMAGE_EXTS = RAW_EXTS | PROCESSED_EXTS
FILE_EXT_NORMALIZATIONS = dict([
    (".jpg", ".jpeg"),
    (".hif", ".heif"),
    (".heic", ".heif")
])

def warn_str(s: str) -> str:
    return f"{click.style("WARNING", fg="yellow")}: {s}"

def error_str(s: str) -> str:
    return f"{click.style("ERROR", fg="red")}: {s}"

def emphasis_str(s: str) -> str:
    return click.style(s, fg="blue")

def collect_image_files(paths: Iterable[pathlib.Path], files_only=False, recurse=False, accepted_suffixes=IMAGE_EXTS) -> Iterable[pathlib.Path]:
    for path in paths:
        if not path.exists():
            continue
        elif path.is_file():
            if path.suffix.lower() in accepted_suffixes:
                yield path
        elif path.is_dir():
            if files_only:
                continue
            else:
                yield from collect_image_files(path.iterdir(), not recurse, recurse, accepted_suffixes=accepted_suffixes)

def read_exif_tag(file: pathlib.Path, tag: str) -> str | None:
    with file.open("rb") as fo:
        try:
            image = exif.Image(fo)
            if image.has_exif:
                return image.get(tag)
            else:
                return None
        except:
            click.echo(warn_str(f"Unable to read EXIF tags on file '{file}'"))
            return None

def normalize_suffix(file: pathlib.Path) -> pathlib.Path:
    file = file.with_suffix(file.suffix.lower())
    if file.suffix in FILE_EXT_NORMALIZATIONS:
        return file.with_suffix(FILE_EXT_NORMALIZATIONS[file.suffix])
    else:
        return file
