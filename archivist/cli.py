import pathlib
import click

from typing import Iterable

from . import canonize_command


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
    canonize_command.canonize(archive, files, move, files_only, recurse, test)

@cli.command()
def clean():
    pass

@cli.command()
def plot():
    pass
