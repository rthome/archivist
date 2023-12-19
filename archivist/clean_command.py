import pathlib
import click

from dataclasses import dataclass
from typing import Iterable

from . import utils
from .count_command import collect_file_suffix_stats


@dataclass
class FileMatch:
    raw_file: pathlib.Path | None
    processed_file: pathlib.Path | None

    @property
    def has_raw(self):
        return self.raw_file is not None
    
    @property
    def has_processed(self):
        return self.processed_file is not None

    @property
    def is_matched(self):
        return self.has_raw and self.has_processed
    
    @property
    def should_remove_raw(self):
        return self.has_raw and not self.has_processed


def find_default_raw_folder(base_folder: pathlib.Path) -> pathlib.Path | None:
    raw_folder_candidate = base_folder / "raw"
    if raw_folder_candidate.is_dir():
        return raw_folder_candidate
    else:
        return None

def find_file_matches(processed_files: Iterable[pathlib.Path], raw_files: Iterable[pathlib.Path], raw_folder: pathlib.Path) -> Iterable[FileMatch]:
    normalized_raw_to_original_raw = {utils.normalize_suffix(r): r for r in raw_files}
    matches = []
    
    for processed_file in processed_files:
        for raw_suffix in utils.RAW_EXTS:
            raw_file_candidate = raw_folder / processed_file.with_suffix(raw_suffix).name
            raw_match = normalized_raw_to_original_raw.pop(raw_file_candidate, None)
            if raw_match:
                matches.append(FileMatch(raw_match, processed_file))
                break
        else:
            # No RAW match found for processed file - add a non-matched entry
            matches.append(FileMatch(None, processed_file))
    
    # Left now are all unmatched RAW files as values in the above dict
    matches.extend((FileMatch(r, None) for r in normalized_raw_to_original_raw.values()))

    return matches

def perform_cleanup():
    pass

def clean(base_folder: pathlib.Path, raw_folder: pathlib.Path | None, test_only: bool):
    if not base_folder.is_dir():
        click.echo(utils.error_str("Base folder doesn't exist. Exiting."))
        return
    
    if raw_folder is None:
        click.echo("No raw folder provided. Searching a suitable default... ", nl=False)
        raw_folder = find_default_raw_folder(base_folder)
        if raw_folder is not None:
            click.echo(utils.emphasis_str("OK"))
        else:
            click.echo()
            click.echo(utils.error_str("No suitable raw image folder found. Exiting."))
            return
    assert raw_folder.is_dir() # This must be true after this point

    click.echo(f"Scanning '{base_folder}' for processed images... ", nl=False)
    processed_image_files = list(utils.collect_image_files([base_folder], recurse=False, accepted_suffixes=utils.PROCESSED_EXTS))
    click.echo(f"found {len(processed_image_files)}.")
    click.echo(f"\t{collect_file_suffix_stats(processed_image_files).format_suffixes()}")

    click.echo(f"Scanning '{raw_folder}' for RAW image files... ", nl=False)
    raw_image_files = list(utils.collect_image_files([raw_folder], recurse=False, accepted_suffixes=utils.RAW_EXTS))
    click.echo(f"found {len(raw_image_files)}.")
    click.echo(f"\t{collect_file_suffix_stats(raw_image_files).format_suffixes()}")

    click.echo("Looking for RAW/processed image file pairs... ", nl=False)
    file_matches = find_file_matches(processed_image_files, raw_image_files, raw_folder)
    click.echo(f"found {len([m for m in file_matches if m.is_matched])}.")

    for match in file_matches:
        click.echo(match)

