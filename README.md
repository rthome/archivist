# Archivist

Personal photo library management scripts (in Python).

## Scripts

- import: Sort image files into an archive folder.
- clean: Remove RAW files whose paired JPEGs have been deleted.
- count: Count image files.
- normalize: Normalizes file extensions to my preferred standard.
- plot: Create a simple plot of focal length distribution for folders of images.

## Install

*Don't*, unless you don't mind some bug deleting your life's work.

Install for example with [pipx](https://github.com/pypa/pipx):

    git clone https://github.com/rthome/archivist.git
    cd archivist
    pipx install .

That will download dependencies and make the application available globally (or at least for the current user). Now, get started with

    archivist --help

