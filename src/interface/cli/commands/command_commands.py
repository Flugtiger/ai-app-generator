import click

from src.application.create_command_handler import CreateCommandHandler, CreateCommandInput
from src.interface.cli.dependency_injection import get_command_repository


@click.group(name="command")
def command_group():
    """
    Commands for managing command definitions.
    """
    pass


@command_group.command(name="create")
@click.option("--name", "-n", required=True, help="The name of the command")
@click.option("--description", "-d", required=True, help="The description of the command")
def create_command(name: str, description: str):
    """
    Create a new command definition.
    """
    # Get dependencies
    command_repository = get_command_repository()
    
    # Create handler
    handler = CreateCommandHandler(command_repository)
    
    # Create input DTO
    input_dto = CreateCommandInput(
        name=name,
        description=description
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Command created successfully with ID: {result.commandId}")