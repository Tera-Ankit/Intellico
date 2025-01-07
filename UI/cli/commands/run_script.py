import os
import click
import subprocess

@click.command()
@click.option('--script', required=True, help='Path to the Python script to execute.')
@click.option('--args', default="", help='Arguments to pass to the Python script.')
def run_script(script, args):
    """
    Run a Python script with optional arguments.
    """
    try:
        # Convert relative script path to absolute
        abs_script = os.path.abspath(script)
        command = f"python {abs_script} {args}"
        print(f"Executing: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing the script: {e}")
