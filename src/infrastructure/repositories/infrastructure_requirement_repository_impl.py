from typing import List

from src.model.infrastructure_requirement.infrastructure_requirement import InfrastructureRequirement
from src.model.infrastructure_requirement.infrastructure_requirement_id import InfrastructureRequirementId
from src.model.infrastructure_requirement.infrastructure_requirement_repository import InfrastructureRequirementRepository
from src.infrastructure.repositories.file_repository import FileRepository


class InfrastructureRequirementRepositoryImpl(InfrastructureRequirementRepository):
    """
    Implementation of InfrastructureRequirementRepository that stores InfrastructureRequirements as JSON files.
    """
    
    def __init__(self):
        """
        Initialize the repository with InfrastructureRequirement class and InfrastructureRequirementId class.
        """
        self.repository = FileRepository(
            entity_class=InfrastructureRequirement,
            id_class=InfrastructureRequirementId,
            folder_name='infrastructure_requirements',
            id_prefix='IR'
        )
    
    def get_by_id(self, id: InfrastructureRequirementId) -> InfrastructureRequirement:
        """
        Retrieves an InfrastructureRequirement by its ID.
        """
        return self.repository.get_by_id(id)
    
    def save(self, infrastructure_requirement: InfrastructureRequirement) -> InfrastructureRequirement:
        """
        Saves an InfrastructureRequirement to the repository.
        """
        return self.repository.save(infrastructure_requirement)
    
    def get_all(self) -> List[InfrastructureRequirement]:
        """
        Retrieves all InfrastructureRequirements from the repository.
        """
        return self.repository.get_all()