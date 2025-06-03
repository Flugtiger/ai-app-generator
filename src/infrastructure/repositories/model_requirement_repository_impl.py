from typing import List

from src.model.model_requirement.model_requirement import ModelRequirement, RequirementState
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.infrastructure.repositories.file_repository import FileRepository


class ModelRequirementRepositoryImpl(ModelRequirementRepository):
    """
    Implementation of ModelRequirementRepository that stores ModelRequirements as JSON files.
    """

    def __init__(self):
        """
        Initialize the repository with ModelRequirement class and ModelRequirementId class.
        """
        self.repository = FileRepository(
            entity_class=ModelRequirement,
            id_class=ModelRequirementId,
            folder_name='model_requirements',
            id_prefix='MR'
        )

    def get_by_id(self, id: ModelRequirementId) -> ModelRequirement:
        """
        Retrieves a ModelRequirement by its ID.
        """
        return self.repository.get_by_id(id)

    def save(self, model_requirement: ModelRequirement) -> ModelRequirement:
        """
        Saves a ModelRequirement to the repository.
        """
        return self.repository.save(model_requirement)

    def get_all(self) -> List[ModelRequirement]:
        """
        Retrieves all ModelRequirements from the repository.
        """
        return self.repository.get_all()

    def get_unimplemented(self) -> List[ModelRequirement]:
        """
        Retrieves all unimplemented ModelRequirements from the repository.
        """
        all_requirements = self.get_all()
        return [req for req in all_requirements if req.state == RequirementState.UNIMPLEMENTED]
