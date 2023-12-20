import pathlib
import click

from itertools import groupby
from typing import Iterable

from . import utils

def normalize(paths: Iterable[pathlib.Path], recurse: bool, test_only: bool):
    # Find files with non-conforming extensions
    click.echo("Collecting image files... ", nl=False)
    image_files = utils.collect_image_files(paths, recurse=recurse)
    normalizable_images = list(filter(lambda p: p.suffix.lower() != p.suffix or p.suffix.lower() in utils.FILE_EXT_NORMALIZATIONS, image_files))
    click.echo(f"found {len(normalizable_images)} normalizable files.")

    if len(normalizable_images) == 0:
        click.echo("No files found. Exiting.")
        return

    # Group by folder
    sorted_normalizable_images = sorted(normalizable_images)
    folder_groups = groupby(sorted_normalizable_images, key=lambda p: p.parent)
    
    # Process files folder by folder
    for current_folder, current_files in folder_groups:
        current_files = list(current_files)
        click.echo(f"Processing {len(current_files)} in '{current_folder}':")
        for file in current_files:
            click.echo("\t", nl=False)
            if test_only:
                click.echo(utils.emphasis_str("TEST "), nl=False)
            normalized_file = utils.normalize_suffix(file)
            click.echo(f"{file.name} -> {normalized_file.name} ", nl=False)
            if normalized_file.exists():
                # TODO: Fails here on Windows if suffix differs in upper/lowercase
                click.echo(f"{utils.emphasis_str("SKIPPED")}: Already exists.")
                continue
            else:
                try:
                    if not test_only:
                        file.rename(normalized_file)
                    click.echo(utils.emphasis_str("OK"))
                except OSError as err:
                    click.echo(utils.error_str(str(err)))
                    click.echo("Exiting.")
                    return
