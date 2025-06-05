import click

from src.application.create_model_requirement_handler import CreateModelRequirementHandler, CreateModelRequirementInput
from src.application.get_model_requirement_handler import GetModelRequirementHandler, GetModelRequirementInput
from src.application.implement_model_requirement_handler import ImplementModelRequirementHandler, ImplementModelRequirementInput
from src.application.update_model_requirement_handler import UpdateModelRequirementHandler, UpdateModelRequirementInput
from src.interface.cli.dependency_injection import (
    get_model_requirement_repository,
    get_domain_model_generator,
    get_domain_model_files_service
)


@click.group(name="model-requirement")
def model_requirement_group():
    """
    Commands for managing model requirements.
    """
    pass


@model_requirement_group.command(name="create")
@click.option("--text", "-t", required=True, help="The text describing the model requirement")
def create_model_requirement(text: str):
    """
    Create a new model requirement.
    """
    # Get dependencies
    model_requirement_repository = get_model_requirement_repository()

    # Create handler
    handler = CreateModelRequirementHandler(model_requirement_repository)

    # Create input DTO
    input_dto = CreateModelRequirementInput(
        requirementText=text
    )

    # Execute handler
    result = handler.handle(input_dto)

    # Output result
    click.echo(f"Model requirement created successfully with ID: {result.modelRequirementId}")


@model_requirement_group.command(name="update")
@click.option("--id", "-i", required=True, help="The ID of the model requirement to update")
@click.option("--text", "-t", required=True, help="The new text describing the model requirement")
def update_model_requirement(id: str, text: str):
    """
    Update an existing model requirement.
    """
    # Get dependencies
    model_requirement_repository = get_model_requirement_repository()

    # Create handler
    handler = UpdateModelRequirementHandler(model_requirement_repository)

    # Create input DTO
    input_dto = UpdateModelRequirementInput(
        requirementId=id,
        requirementText=text
    )

    # Execute handler
    result = handler.handle(input_dto)

    # Output result
    click.echo(f"Model requirement {result.modelRequirementId} updated successfully.")
    click.echo(f"Current state: {result.state}")


@model_requirement_group.command(name="get")
@click.option("--id", "-i", required=True, help="The ID of the model requirement to retrieve")
def get_model_requirement(id: str):
    """
    Retrieve a model requirement by its ID.
    """
    # Get dependencies
    model_requirement_repository = get_model_requirement_repository()

    # Create handler
    handler = GetModelRequirementHandler(model_requirement_repository)

    # Create input DTO
    input_dto = GetModelRequirementInput(
        modelRequirementId=id
    )

    # Execute handler
    result = handler.handle(input_dto)

    # Output result
    click.echo(f"Model Requirement ID: {result.modelRequirementId}")
    click.echo(f"Text: {result.requirementText}")
    click.echo(f"State: {result.state}")


@model_requirement_group.command(name="implement")
@click.option("--id", "-i", required=True, help="The ID of the model requirement to implement")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def implement_model_requirement(id: str, target_dir: str):
    """
    Implement a single model requirement in the domain model.
    """
    # Get dependencies
    model_requirement_repository = get_model_requirement_repository()
    domain_model_generator = get_domain_model_generator()
    domain_model_files_service = get_domain_model_files_service()

    # Create handler
    handler = ImplementModelRequirementHandler(
        model_requirement_repository,
        domain_model_generator,
        domain_model_files_service
    )

    # Create input DTO
    input_dto = ImplementModelRequirementInput(
        requirementId=id,
        targetDirectory=target_dir
    )

    # Execute handler
    result = handler.handle(input_dto)

    # Output result
    click.echo(f"Model requirement {result.requirementId} implemented successfully.")
    click.echo(f"Number of files affected: {result.numberOfFiles}")
