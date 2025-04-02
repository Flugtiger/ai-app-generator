import click

from src.application.generate_model_handler import GenerateModelHandler, GenerateModelInput
from src.application.generate_application_handler import GenerateApplicationHandler, GenerateApplicationInput
from src.application.generate_infrastructure_handler import GenerateInfrastructureHandler, GenerateInfrastructureInput
from src.application.generate_interface_handler import GenerateInterfaceHandler, GenerateInterfaceInput
from src.application.generate_project_handler import GenerateProjectHandler, GenerateProjectInput
from src.interface.cli.dependency_injection import (
    get_model_requirement_repository,
    get_command_repository,
    get_infrastructure_requirement_repository,
    get_domain_model_generator,
    get_application_generator,
    get_infrastructure_generator,
    get_interface_generator,
    get_project_generator,
    get_domain_model_files_service,
    get_application_files_service,
    get_infrastructure_files_service,
    get_interface_files_service
)


@click.group(name="generate")
def generate_group():
    """
    Commands for generating code.
    """
    pass


@generate_group.command(name="model")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_model(target_dir: str):
    """
    Generate domain model code from requirements.
    """
    # Get dependencies
    model_requirement_repository = get_model_requirement_repository()
    domain_model_generator = get_domain_model_generator()
    domain_model_files_service = get_domain_model_files_service()
    
    # Create handler
    handler = GenerateModelHandler(
        model_requirement_repository,
        domain_model_generator,
        domain_model_files_service
    )
    
    # Create input DTO
    input_dto = GenerateModelInput(
        targetDirectory=target_dir
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Domain model generated successfully with {result.numberOfFiles} files in {target_dir}")


@generate_group.command(name="application")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_application(target_dir: str):
    """
    Generate application layer code from commands and domain model.
    """
    # Get dependencies
    command_repository = get_command_repository()
    application_generator = get_application_generator()
    domain_model_files_service = get_domain_model_files_service()
    application_files_service = get_application_files_service()
    
    # Create handler
    handler = GenerateApplicationHandler(
        command_repository,
        application_generator,
        domain_model_files_service,
        application_files_service
    )
    
    # Create input DTO
    input_dto = GenerateApplicationInput(
        targetDirectory=target_dir
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Application layer generated successfully with {result.numberOfFiles} files in {target_dir}")


@generate_group.command(name="infrastructure")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_infrastructure(target_dir: str):
    """
    Generate infrastructure code from requirements and domain model.
    """
    # Get dependencies
    infrastructure_requirement_repository = get_infrastructure_requirement_repository()
    infrastructure_generator = get_infrastructure_generator()
    domain_model_files_service = get_domain_model_files_service()
    infrastructure_files_service = get_infrastructure_files_service()
    
    # Create handler
    handler = GenerateInfrastructureHandler(
        infrastructure_requirement_repository,
        infrastructure_generator,
        domain_model_files_service,
        infrastructure_files_service
    )
    
    # Create input DTO
    input_dto = GenerateInfrastructureInput(
        targetDirectory=target_dir
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Infrastructure code generated successfully with {result.numberOfFiles} files in {target_dir}")


@generate_group.command(name="interface")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_interface(target_dir: str):
    """
    Generate interface code from domain model, application and infrastructure code.
    """
    # Get dependencies
    interface_generator = get_interface_generator()
    domain_model_files_service = get_domain_model_files_service()
    application_files_service = get_application_files_service()
    infrastructure_files_service = get_infrastructure_files_service()
    interface_files_service = get_interface_files_service()
    
    # Create handler
    handler = GenerateInterfaceHandler(
        interface_generator,
        domain_model_files_service,
        application_files_service,
        infrastructure_files_service,
        interface_files_service
    )
    
    # Create input DTO
    input_dto = GenerateInterfaceInput(
        targetDirectory=target_dir
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Interface code generated successfully with {result.numberOfFiles} files in {target_dir}")


@generate_group.command(name="project")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_project(target_dir: str):
    """
    Generate project files from infrastructure and interface code.
    """
    # Get dependencies
    project_generator = get_project_generator()
    infrastructure_files_service = get_infrastructure_files_service()
    interface_files_service = get_interface_files_service()
    
    # Create handler
    handler = GenerateProjectHandler(
        project_generator,
        infrastructure_files_service,
        interface_files_service
    )
    
    # Create input DTO
    input_dto = GenerateProjectInput(
        targetDirectory=target_dir
    )
    
    # Execute handler
    result = handler.handle(input_dto)
    
    # Output result
    click.echo(f"Project files generated successfully with {result.numberOfFiles} files in {target_dir}")


@generate_group.command(name="all")
@click.option("--target-dir", "-t", default="generated", help="The directory where the generated files will be written")
def generate_all(target_dir: str):
    """
    Generate all code (model, application, infrastructure, interface, project).
    """
    # Generate each layer in sequence
    generate_model.callback(target_dir)
    generate_application.callback(target_dir)
    generate_infrastructure.callback(target_dir)
    generate_interface.callback(target_dir)
    generate_project.callback(target_dir)
    
    click.echo(f"All code generated successfully in {target_dir}")