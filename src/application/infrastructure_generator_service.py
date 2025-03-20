from pydantic import BaseModel
from typing import List, Optional

from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.infra_requirement.infra_requirement_id import InfraRequirementId
from src.model.infra_requirement.infra_requirement_repository import InfraRequirementRepository
from src.model.services.infrastructure_generator.infrastructure_generator import InfrastructureGenerator
from src.model.services.domain_model_service import DomainModelService
from src.model.value_objects.infrastructure_files import InfrastructureFiles


class GenerateInfrastructureInput(BaseModel):
    """
    Input data for generating infrastructure code.
    """
    project_path: str
    requirement_ids: Optional[List[str]] = None


class GenerateInfrastructureOutput(BaseModel):
    """
    Output data after generating infrastructure code.
    """
    files_count: int
    project_path: str


class InfrastructureGeneratorCommands:
    """
    Application service for infrastructure generation commands.
    """

    def __init__(
        self,
        infra_requirement_repository: InfraRequirementRepository,
        infrastructure_generator: InfrastructureGenerator
    ):
        """
        Initialize the application service with required dependencies.

        Args:
            infra_requirement_repository: Repository for infrastructure requirements.
            infrastructure_generator: Service for generating infrastructure code.
        """
        self.infra_requirement_repository = infra_requirement_repository
        self.infrastructure_generator = infrastructure_generator

    def generate_infrastructure(self, input_data: GenerateInfrastructureInput) -> GenerateInfrastructureOutput:
        """
        Generate infrastructure code based on requirements.

        Args:
            input_data: Input data containing project path and optional requirement IDs.

        Returns:
            Output data containing the number of files generated and the project path.
        """
        # Get all requirements if no specific IDs are provided
        if input_data.requirement_ids is None or len(input_data.requirement_ids) == 0:
            requirements = self.infra_requirement_repository.get_all()
        else:
            # Get specific requirements by ID
            requirements = []
            for req_id_str in input_data.requirement_ids:
                req_id = InfraRequirementId(value=req_id_str)
                requirement = self.infra_requirement_repository.get_by_id(req_id)
                if requirement:
                    requirements.append(requirement)

        if not requirements:
            raise ValueError("No infrastructure requirements found")

        # Read the existing domain model from the project
        domain_model = DomainModelService.read_from_directory(input_data.project_path)

        # Generate the infrastructure code
        infrastructure_files = self.infrastructure_generator.generate_infrastructure(
            requirements=requirements,
            domain_model=domain_model
        )

        # Write the generated files to the project directory
        DomainModelService.write_to_directory(
            infrastructure_files,
            input_data.project_path,
            create_dirs=True
        )

        # Return the output
        return GenerateInfrastructureOutput(
            files_count=len(infrastructure_files.files),
            project_path=input_data.project_path
        )
