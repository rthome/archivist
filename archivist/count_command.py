import pathlib
import click

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Tuple

from . import utils


@dataclass
class SuffixStats:
    total_count: int
    suffix_counts: Iterable[Tuple[str, int]]

    def format_suffixes(self) -> str:
        return ", ".join([f"{p[0]}: {p[1]}" for p in self.suffix_counts])
    
    def format_total(self) -> str:
        return f"TOTAL: {self.total_count}"


def collect_file_suffix_stats(files: Iterable[pathlib.Path]) -> SuffixStats:
    suffixes = (file.suffix for file in files)
    suffix_counter = Counter(suffixes)
    return SuffixStats(sum(suffix_counter.values()), suffix_counter.most_common())

def count(paths: Iterable[pathlib.Path], normalize: bool):
    image_files = utils.collect_image_files(paths, recurse=True)
    if normalize:
        image_files = map(utils.normalize_suffix, image_files)
    stats = collect_file_suffix_stats(image_files)
    click.echo(stats.format_suffixes())
    click.echo(stats.format_total())
