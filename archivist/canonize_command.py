import datetime, pathlib, shutil
import click

from dataclasses import dataclass
from typing import Iterable

from . import utils


@dataclass
class ImportOperation:
    original_path: pathlib.Path
    canonical_path: pathlib.Path

@dataclass
class ImportFile:
    path: pathlib.Path
    capture_time: datetime.datetime

def read_datetime(file: pathlib.Path) -> datetime.datetime | None:
    exif_data = utils.read_exif_tag(file, "datetime_original")
    if exif_data is None:
        return None
    else:
        return datetime.datetime.strptime(exif_data, "%Y:%m:%d %H:%M:%S")

def process_input_files(image_files: Iterable[pathlib.Path]) -> Iterable[ImportFile]:
    import_files = []
    with click.progressbar(image_files, label="Reading EXIF tags") as bar:
        for image_file in bar:
            capture_time = read_datetime(image_file)
            if capture_time is None:
                click.echo(utils.CC.warn(f"No capture time on file '{image_file}' - skipping."))
                continue
            import_files.append(ImportFile(image_file, capture_time))
        return import_files

def make_import_operations(archive: pathlib.Path, files: Iterable[ImportFile]) -> Iterable[ImportOperation]:
    def normalize_suffix(file: pathlib.Path):
        if file.suffix.lower() in utils.FILE_EXT_NORMALIZATIONS:
            return file.with_suffix(utils.FILE_EXT_NORMALIZATIONS[file.suffix.lower()])
        else:
            return file
    
    import_operations = []
    name_counts = dict()
    for file in files:
        canonical_file_name = file.capture_time.strftime("%Y%m%d_%H_%M_%S") + file.suffix.lower()
        if canonical_file_name in name_counts:
            ncount = name_counts[canonical_file_name]
            name_counts[canonical_file_name] += 1
            canonical_file_name = file.capture_time.strftime("%Y%m%d_%H_%M_%S") + f"-{ncount}" + file.suffix.lower()
        else:
            name_counts[canonical_file_name] = 1
        canonical_path = normalize_suffix(archive / file.capture_time.strftime("%Y") / file.capture_time.strftime("%m") / canonical_file_name)
        import_operations.append(ImportOperation(file.path, canonical_path))
    return import_operations

def perform_import(import_operations: Iterable[ImportOperation], move_files: bool, test_only: bool) -> None:
    operation = utils.CC.orange("MOVE" if move_files else "COPY")
    if test_only:
        operation = utils.CC.orange("TEST") + " " + operation
    with click.progressbar(import_operations, label="Importing") as bar:
        for import_op in bar:
            click.echo(f"{operation} {import_op.original_path} {utils.CC.orange("TO")} {import_op.canonical_path}")
            if not test_only:
                if not import_op.canonical_path.parent.exists():
                    import_op.canonical_path.parent.mkdir(parents=True)
                shutil.copy2(import_op.original_path, import_op.canonical_path)
                if move_files:
                    import_op.original_path.unlink()

def canonize(archive: pathlib.Path,
             import_items: Iterable[pathlib.Path],
             move_files: bool,
             files_only: bool,
             recursive_search: bool,
             test_only: bool) -> None:
    if not archive.is_dir() or not archive.exists():
        click.echo(utils.CC.error("Archive path not a directory or doesn't exist. Exiting."))
        return
    
    click.echo("Collecting files... ", nl=False)
    image_files = list(utils.collect_image_files(import_items, files_only, recursive_search, utils.IMAGE_EXTS))
    click.echo(f"found {len(image_files)} files.")

    if len(image_files) == 0:
        click.echo("No files found - exiting.")
        return

    click.echo("Processing image files...")
    import_files = process_input_files(image_files)
    import_operations = make_import_operations(archive, import_files)

    click.echo("Importing files...")
    perform_import(import_operations, move_files, test_only)

    click.echo("Done.")
