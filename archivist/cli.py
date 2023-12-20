import pathlib
import click

from typing import Iterable

from . import import_command, clean_command, count_command, normalize_command, plot_command


@click.group()
@click.version_option()
def cli():
    pass

@cli.command(name="import")
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-a", "--archive", default=".", type=click.Path(file_okay=False, path_type=pathlib.Path), help="Path to the archive directory")
@click.option("-t", "--test", is_flag=True, help="Print proposed actions, but don't actually do anything")
@click.option("-m", "--move", is_flag=True, help="Move files instead of copying them (CARE: deletes the originals)")
@click.option("-o", "--files-only", is_flag=True, help="Only process file paths, ignore any given directory paths")
@click.option("-r", "--recurse", is_flag=True, help="Read image files recursively from any given directories")
def import_files(files: Iterable[pathlib.Path], archive: pathlib.Path, test: bool, move: bool, files_only: bool, recurse: bool):
    """Collect image files and import them into an archive folder, according to their capture date and time."""
    import_command.import_files(archive, files, move, files_only, recurse, test)

@cli.command()
@click.argument("processed_images_dir", nargs=1, default=".", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("-d", "--raw-dir", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path), help="Directory containing RAW image files to be cleaned up")
@click.option("-t", "--test", is_flag=True, help="Print proposed actions, but don't actually do anything")
def clean(processed_images_dir: pathlib.Path, raw_dir: pathlib.Path | None, test: bool):
    """
    Clean up raw image files whose paired jpegs have been deleted.

    By default, processed images will be collected from the current working directory.
    If --raw-dir isn't given, this command will look for a suitable folder of RAW images -
    such as a subfolder of the PROCESSED_IMAGES_DIR named "raw".
    """
    clean_command.clean(processed_images_dir, raw_dir, test)

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
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-r", "--recurse", is_flag=True, help="Read image files recursively from any given directories")
@click.option("-t", "--test", is_flag=True, help="Print proposed actions, but don't actually do anything")
def normalize(paths: Iterable[pathlib.Path], recurse: bool, test: bool):
    """
    Normalize file extensions by renaming (image) files (e.g. .JPG -> .jpeg), while attempting to preserve file attributes.
    
    Works with any number of file or directory path arguments. Everything will be renamed in-place.
    """
    normalize_command.normalize(paths, recurse, test)

@cli.command()
@click.argument("folders", nargs=-1,  type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("-o", "--out-file", type=click.Path(dir_okay=False, path_type=pathlib.Path), help="Save the generated plot to the given file path (instead of opening it straight away)")
@click.option("-r", "--raw-only", is_flag=True, help="Only read data from raw file formats (such as .RAF, .NEF, etc.)")
@click.option("-p", "--processed-only", is_flag=True, help="Only read data from processed file formats (such as JPEG)")
def plot(folders: Iterable[pathlib.Path], out_file: pathlib.Path | None, raw_only: bool, processed_only: bool):
    """Plot focal length distribution of image files."""
    plot_command.plot(folders, out_file, raw_only, processed_only)
