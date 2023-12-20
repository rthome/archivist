import pathlib
import click, exif
import plotly.graph_objects as go

from collections import Counter
from typing import Iterable

from . import utils
from .count_command import collect_file_suffix_stats

def collect_focal_lengths(files: Iterable[pathlib.Path]) -> Iterable[str]:
    def collect(file: pathlib.Path) -> str | None:
        with file.open("rb") as fo:
            try:
                image = exif.Image(fo)
            except:
                click.echo(utils.warn_str(f"Unable to read file '{file}'. Skipping..."))
                return None
        if not image.has_exif:
            click.echo(utils.warn_str(f"No EXIF tags in file '{file}'. Skipping..."))
            return None
        else:
            try:
                return image.focal_length_in_35mm_film
            except:
                click.echo(utils.warn_str(f"No 'focal_length_in_35mm_film' EXIF tag in file '{file}'. Skipping..."))
                return None
    return [collect(f) for f in files]

def generate_graph(out_file : pathlib.Path | None, focal_lengths: Iterable):
    counts = Counter(sorted(focal_lengths))

    x = [f"{focal_len}mm" for focal_len in counts.keys()]
    y = list(counts.values())

    fig = go.Figure(data=[go.Bar(x=x, y=y,
                                 text=y, 
                                 textposition="auto")],
                    layout_title_text=f"Focal lengths for {len(focal_lengths)} images:")
    fig.update_layout(xaxis_tickangle=-45)

    if out_file is not None:
        target_file = out_file.with_suffix(".html")
        fig.write_html(file=target_file)
        click.echo(f"{utils.emphasis_str("Saved plot to")} '{target_file}'.")
    else:
        fig.show()

def plot(folders: Iterable[pathlib.Path], out_file: pathlib.Path | None, raw_only: bool, processed_only: bool):
    accepted_suffixes = set()
    if not raw_only:
        accepted_suffixes |= utils.PROCESSED_EXTS
    if not processed_only:
        accepted_suffixes |= utils.RAW_EXTS

    click.echo("Collecting image files... ", nl=False)
    image_files = list(utils.collect_image_files(folders, recurse=True, accepted_suffixes=accepted_suffixes))
    click.echo(f"found {len(image_files)}.")
    click.echo(f"  {collect_file_suffix_stats(image_files).format_suffixes()}")

    click.echo("Collecting focal lengths... ", nl=False)
    focal_length_data = collect_focal_lengths(image_files)
    click.echo(f"found {len(focal_length_data)}.")

    generate_graph(out_file, focal_length_data)
