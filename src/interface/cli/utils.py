"""
Utility functions for the CLI interface.
"""
import os
import click


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that the specified directory exists, creating it if necessary.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        click.echo(f"Created directory: {directory_path}")