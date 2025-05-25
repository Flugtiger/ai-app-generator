#!/usr/bin/env python3
import time
import click
import sys
import traceback

from src.interface.cli.commands.command_commands import command_group
from src.interface.cli.commands.model_requirement_commands import model_requirement_group
from src.interface.cli.commands.infrastructure_requirement_commands import infrastructure_requirement_group
from src.interface.cli.commands.generate_commands import generate_group


@click.group()
def cli():
    """
    Command-line interface for the DDD code generator application.
    """
    pass


# Add command groups to the main CLI
cli.add_command(command_group)
cli.add_command(model_requirement_group)
cli.add_command(infrastructure_requirement_group)
cli.add_command(generate_group)


def main():
    """
    Main entry point for the CLI application.
    Catches all unhandled exceptions and prints stack traces.
    """
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("\nStack trace:", err=True)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
