"""
Module for dependency injection in the CLI interface.
Provides factory functions for all required dependencies.
"""
from src.model.command.command_repository import CommandRepository
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.infrastructure_requirement.infrastructure_requirement_repository import InfrastructureRequirementRepository
from src.model.generators.domain_model_generator import DomainModelGenerator
from src.model.generators.application_generator import ApplicationGenerator
from src.model.generators.infrastructure_generator import InfrastructureGenerator
from src.model.generators.interface_generator import InterfaceGenerator
from src.model.generators.project_generator import ProjectGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.infrastructure_files_service import InfrastructureFilesService
from src.model.services.interface_files_service import InterfaceFilesService
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser
from src.model.services.code_compressor import CodeCompressor

from src.infrastructure.repositories.command_repository_impl import CommandRepositoryImpl
from src.infrastructure.repositories.model_requirement_repository_impl import ModelRequirementRepositoryImpl
from src.infrastructure.repositories.infrastructure_requirement_repository_impl import InfrastructureRequirementRepositoryImpl
from src.infrastructure.services.llm_service_impl import LLMServiceImpl
from src.infrastructure.services.message_parser_impl import MessageParserImpl
from src.infrastructure.services.code_compressor_impl import CodeCompressorImpl


# Singleton instances
_command_repository = None
_model_requirement_repository = None
_infrastructure_requirement_repository = None
_llm_service = None
_message_parser = None
_code_compressor = None
_domain_model_generator = None
_application_generator = None
_infrastructure_generator = None
_interface_generator = None
_project_generator = None
_domain_model_files_service = None
_application_files_service = None
_infrastructure_files_service = None
_interface_files_service = None


def get_command_repository() -> CommandRepository:
    """
    Get or create the CommandRepository instance.
    """
    global _command_repository
    if _command_repository is None:
        _command_repository = CommandRepositoryImpl()
    return _command_repository


def get_model_requirement_repository() -> ModelRequirementRepository:
    """
    Get or create the ModelRequirementRepository instance.
    """
    global _model_requirement_repository
    if _model_requirement_repository is None:
        _model_requirement_repository = ModelRequirementRepositoryImpl()
    return _model_requirement_repository


def get_infrastructure_requirement_repository() -> InfrastructureRequirementRepository:
    """
    Get or create the InfrastructureRequirementRepository instance.
    """
    global _infrastructure_requirement_repository
    if _infrastructure_requirement_repository is None:
        _infrastructure_requirement_repository = InfrastructureRequirementRepositoryImpl()
    return _infrastructure_requirement_repository


def get_llm_service() -> LLMService:
    """
    Get or create the LLMService instance.
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMServiceImpl()
    return _llm_service


def get_message_parser() -> MessageParser:
    """
    Get or create the MessageParser instance.
    """
    global _message_parser
    if _message_parser is None:
        _message_parser = MessageParserImpl()
    return _message_parser


def get_code_compressor() -> CodeCompressor:
    """
    Get or create the CodeCompressor instance.
    """
    global _code_compressor
    if _code_compressor is None:
        _code_compressor = CodeCompressorImpl()
    return _code_compressor


def get_domain_model_generator() -> DomainModelGenerator:
    """
    Get or create the DomainModelGenerator instance.
    """
    global _domain_model_generator
    if _domain_model_generator is None:
        _domain_model_generator = DomainModelGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _domain_model_generator


def get_application_generator() -> ApplicationGenerator:
    """
    Get or create the ApplicationGenerator instance.
    """
    global _application_generator
    if _application_generator is None:
        _application_generator = ApplicationGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _application_generator


def get_infrastructure_generator() -> InfrastructureGenerator:
    """
    Get or create the InfrastructureGenerator instance.
    """
    global _infrastructure_generator
    if _infrastructure_generator is None:
        _infrastructure_generator = InfrastructureGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _infrastructure_generator


def get_interface_generator() -> InterfaceGenerator:
    """
    Get or create the InterfaceGenerator instance.
    """
    global _interface_generator
    if _interface_generator is None:
        _interface_generator = InterfaceGenerator(
            get_llm_service(),
            get_message_parser(),
            get_code_compressor()
        )
    return _interface_generator


def get_project_generator() -> ProjectGenerator:
    """
    Get or create the ProjectGenerator instance.
    """
    global _project_generator
    if _project_generator is None:
        _project_generator = ProjectGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _project_generator


def get_domain_model_files_service() -> DomainModelFilesService:
    """
    Get or create the DomainModelFilesService instance.
    """
    global _domain_model_files_service
    if _domain_model_files_service is None:
        _domain_model_files_service = DomainModelFilesService()
    return _domain_model_files_service


def get_application_files_service() -> ApplicationFilesService:
    """
    Get or create the ApplicationFilesService instance.
    """
    global _application_files_service
    if _application_files_service is None:
        _application_files_service = ApplicationFilesService()
    return _application_files_service


def get_infrastructure_files_service() -> InfrastructureFilesService:
    """
    Get or create the InfrastructureFilesService instance.
    """
    global _infrastructure_files_service
    if _infrastructure_files_service is None:
        _infrastructure_files_service = InfrastructureFilesService()
    return _infrastructure_files_service


def get_interface_files_service() -> InterfaceFilesService:
    """
    Get or create the InterfaceFilesService instance.
    """
    global _interface_files_service
    if _interface_files_service is None:
        _interface_files_service = InterfaceFilesService()
    return _interface_files_service