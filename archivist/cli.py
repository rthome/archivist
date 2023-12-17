import click

from . import canonize, clean, plot

@click.group()
def cli():
    pass

@cli.command()
def canonize():
    pass

@cli.command()
def clean():
    pass

@cli.command()
def plot():
    pass
