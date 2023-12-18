import pathlib
import click

from typing import Iterable

from . import canonize_command
from . import clean_command
from . import count_command
from . import plot_command


@click.group()
def cli():
    pass

@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-a", "--archive", default=".", type=click.Path(file_okay=False, path_type=pathlib.Path), help="Path to the archive directory")
@click.option("-t", "--test", is_flag=True, help="Print proposed actions, but don't actually do anything")
@click.option("-m", "--move", is_flag=True, help="Move files instead of copying them (CARE: deletes the originals)")
@click.option("-o", "--files-only", is_flag=True, help="Only process file paths, ignore any given directory paths")
@click.option("-r", "--recurse", is_flag=True, help="Read image files recursively from any given directories")
def canonize(files: Iterable[pathlib.Path], archive: pathlib.Path, test: bool, move: bool, files_only: bool, recurse: bool):
    """Collect image files and sort them into an archive folder, according to their capture date and time."""
    canonize_command.canonize(archive, files, move, files_only, recurse, test)

@cli.command()
@click.argument("processed_images_dir", nargs=1, default=".", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("-d", "--raw-dir", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path), help="Directory containing RAW image files to be cleaned up")
@click.option("-r", "--recurse", is_flag=True, help="Read image files recursively from any given directories")
@click.option("-t", "--test", is_flag=True, help="Print proposed actions, but don't actually do anything")
def clean(processed_images_dir: pathlib.Path, raw_dir: pathlib.Path | None, recurse: bool, test: bool):
    """
    Clean up raw image files whose paired jpegs have been deleted.

    By default, processed images will be collected from the current working directory.
    If --raw-dir isn't given, this command will look for a suitable folder of RAW images -
    such as a subfolder of the PROCESSED_IMAGES_DIR named "raw".
    """
    clean_command.clean(processed_images_dir, raw_dir, recurse, test)

@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-n/-l", "--normalize/--no-normalize", default=True, help="Normalize file suffixes, e.g. .JPG -> .jpeg")
def count(paths: Iterable[pathlib.Path], normalize: bool):
    """
    Count image files found under the given paths.
    
    Both directory as well as file paths can be passed to this command - it'll sum it all up.
    File suffixes will be normalized by default so as not to end up with a statistic full of .JPG, .jpg, .jpeg, and so on.
    """
    count_command.count(paths, normalize)

@cli.command()
def plot():
    """Plot focal length distribution of image files."""
    pass
