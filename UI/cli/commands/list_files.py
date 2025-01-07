import click
import os

@click.command()
@click.option('--dir', default='.', help='Directory to list files from.')
def list_files(dir):
    """List all files in the specified directory."""
    if not os.path.exists(dir):
        click.echo(f"Error: Directory '{dir}' does not exist.")
        return
    files = os.listdir(dir)
    if not files:
        click.echo(f"No files found in '{dir}'.")
    else:
        click.echo(f"Files in '{dir}':")
        for file in files:
            click.echo(f"  - {file}")
