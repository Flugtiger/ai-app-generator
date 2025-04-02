import click

from src.application.create_infrastructure_requirement_handler import (
    CreateInfrastructureRequirementHandler,
    CreateInfrastructureRequirementInput
)
from src.interface.cli.dependency_injection import get_infrastructure_requirement_repository


@click.group(name="infrastructure-requirement")
def infrastructure_requirement_group():
    """
    Commands for managing infrastructure requirements.
    """
    pass


@infrastructure_requirement_group.command(name="create")
@click.option("--text", "-t", required=True, help="The text describing the infrastructure requirement")
def create_infrastructure_requirement(text: str):
    """
    Create a new infrastructure requirement.
    """
    # Get dependencies
    infrastructure_requirement_repository = get_infrastructure_requirement_repository()
    
    # Create handler
    handler = CreateInfrastructureRequirementHandler(infrastructure_requirement_repository)
    
    # Create input DTO
    input_dto = CreateInfrastructureRequirementInput(
        requirementText=text
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Infrastructure requirement created successfully with ID: {result.infrastructureRequirementId}")