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

class CC(object):
    X = '\033[0m'  # clear
    O = '\033[33m' # orange
    R = '\033[31m' # red
    Y = '\033[93m' # yellow

    @classmethod
    def _fmt(cls, color, s):
        return color + str(s) + cls.X

    @classmethod
    def red(cls, s):
        return cls._fmt(cls.R, s)
    
    @classmethod
    def orange(cls, s):
        return cls._fmt(cls.O, s)

    @classmethod
    def yellow(cls, s):
        return cls._fmt(cls.Y, s)
    
    @classmethod
    def warn(cls, s: str) -> str:
        return f"{CC.yellow("Warning")}: {s}"
    
    def error(cls, s: str) -> str:
        return f"{CC.red("Error")}: {s}"
    

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
                yield from collect_image_files(path.iterdir(), not recurse, recurse)

def read_exif_tag(file: pathlib.Path, tag: str) -> str | None:
    with file.open("rb") as fo:
        try:
            image = exif.Image(fo)
            if image.has_exif:
                return image.get(tag)
            else:
                return None
        except:
            click.echo(CC.warn(f"Unable to read EXIF tags on file '{file}'"))
            return None
