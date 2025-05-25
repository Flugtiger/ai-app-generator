"""
Module for dependency injection in the CLI interface.
Provides factory functions for all required dependencies.
Uses lazy imports to speed up application startup time.
"""
import time
import importlib
from typing import Any, TypeVar, Type

# Type definitions for better type hinting
T = TypeVar('T')


def lazy_import(module_path: str, class_name: str) -> Type[Any]:
    """
    Lazily import a class from a module path.

    Args:
        module_path: The path to the module
        class_name: The name of the class to import

    Returns:
        The imported class
    """
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


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


def get_command_repository():
    """
    Get or create the CommandRepository instance.
    """
    global _command_repository
    if _command_repository is None:
        CommandRepository = lazy_import("src.model.command.command_repository", "CommandRepository")
        CommandRepositoryImpl = lazy_import(
            "src.infrastructure.repositories.command_repository_impl", "CommandRepositoryImpl")
        _command_repository = CommandRepositoryImpl()
    return _command_repository


def get_model_requirement_repository():
    """
    Get or create the ModelRequirementRepository instance.
    """
    global _model_requirement_repository
    if _model_requirement_repository is None:
        ModelRequirementRepository = lazy_import(
            "src.model.model_requirement.model_requirement_repository", "ModelRequirementRepository")
        ModelRequirementRepositoryImpl = lazy_import(
            "src.infrastructure.repositories.model_requirement_repository_impl", "ModelRequirementRepositoryImpl")
        _model_requirement_repository = ModelRequirementRepositoryImpl()
    return _model_requirement_repository


def get_infrastructure_requirement_repository():
    """
    Get or create the InfrastructureRequirementRepository instance.
    """
    global _infrastructure_requirement_repository
    if _infrastructure_requirement_repository is None:
        InfrastructureRequirementRepository = lazy_import(
            "src.model.infrastructure_requirement.infrastructure_requirement_repository", "InfrastructureRequirementRepository")
        InfrastructureRequirementRepositoryImpl = lazy_import(
            "src.infrastructure.repositories.infrastructure_requirement_repository_impl", "InfrastructureRequirementRepositoryImpl")
        _infrastructure_requirement_repository = InfrastructureRequirementRepositoryImpl()
    return _infrastructure_requirement_repository


def get_llm_service():
    """
    Get or create the LLMService instance.
    """
    global _llm_service
    if _llm_service is None:
        LLMService = lazy_import("src.model.services.llm_service", "LLMService")
        LLMServiceImpl = lazy_import("src.infrastructure.services.llm_service_impl", "LLMServiceImpl")
        _llm_service = LLMServiceImpl()
    return _llm_service


def get_message_parser():
    """
    Get or create the MessageParser instance.
    """
    global _message_parser
    if _message_parser is None:
        MessageParser = lazy_import("src.model.services.message_parser", "MessageParser")
        MessageParserImpl = lazy_import("src.infrastructure.services.message_parser_impl", "MessageParserImpl")
        _message_parser = MessageParserImpl()
    return _message_parser


def get_code_compressor():
    """
    Get or create the CodeCompressor instance.
    """
    global _code_compressor
    if _code_compressor is None:
        CodeCompressor = lazy_import("src.model.services.code_compressor", "CodeCompressor")
        CodeCompressorImpl = lazy_import("src.infrastructure.services.code_compressor_impl", "CodeCompressorImpl")
        _code_compressor = CodeCompressorImpl()
    return _code_compressor


def get_domain_model_generator():
    """
    Get or create the DomainModelGenerator instance.
    """
    global _domain_model_generator
    if _domain_model_generator is None:
        DomainModelGenerator = lazy_import("src.model.generators.domain_model_generator", "DomainModelGenerator")
        _domain_model_generator = DomainModelGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _domain_model_generator


def get_application_generator():
    """
    Get or create the ApplicationGenerator instance.
    """
    global _application_generator
    if _application_generator is None:
        ApplicationGenerator = lazy_import("src.model.generators.application_generator", "ApplicationGenerator")
        _application_generator = ApplicationGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _application_generator


def get_infrastructure_generator():
    """
    Get or create the InfrastructureGenerator instance.
    """
    global _infrastructure_generator
    if _infrastructure_generator is None:
        InfrastructureGenerator = lazy_import(
            "src.model.generators.infrastructure_generator", "InfrastructureGenerator")
        _infrastructure_generator = InfrastructureGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _infrastructure_generator


def get_interface_generator():
    """
    Get or create the InterfaceGenerator instance.
    """
    global _interface_generator
    if _interface_generator is None:
        InterfaceGenerator = lazy_import("src.model.generators.interface_generator", "InterfaceGenerator")
        _interface_generator = InterfaceGenerator(
            get_llm_service(),
            get_message_parser(),
            get_code_compressor()
        )
    return _interface_generator


def get_project_generator():
    """
    Get or create the ProjectGenerator instance.
    """
    global _project_generator
    if _project_generator is None:
        ProjectGenerator = lazy_import("src.model.generators.project_generator", "ProjectGenerator")
        _project_generator = ProjectGenerator(
            get_llm_service(),
            get_message_parser()
        )
    return _project_generator


def get_domain_model_files_service():
    """
    Get or create the DomainModelFilesService instance.
    """
    global _domain_model_files_service
    if _domain_model_files_service is None:
        DomainModelFilesService = lazy_import(
            "src.model.services.domain_model_files_service", "DomainModelFilesService")
        _domain_model_files_service = DomainModelFilesService()
    return _domain_model_files_service


def get_application_files_service():
    """
    Get or create the ApplicationFilesService instance.
    """
    global _application_files_service
    if _application_files_service is None:
        ApplicationFilesService = lazy_import("src.model.services.application_files_service", "ApplicationFilesService")
        _application_files_service = ApplicationFilesService()
    return _application_files_service


def get_infrastructure_files_service():
    """
    Get or create the InfrastructureFilesService instance.
    """
    global _infrastructure_files_service
    if _infrastructure_files_service is None:
        InfrastructureFilesService = lazy_import(
            "src.model.services.infrastructure_files_service", "InfrastructureFilesService")
        _infrastructure_files_service = InfrastructureFilesService()
    return _infrastructure_files_service


def get_interface_files_service():
    """
    Get or create the InterfaceFilesService instance.
    """
    global _interface_files_service
    if _interface_files_service is None:
        InterfaceFilesService = lazy_import("src.model.services.interface_files_service", "InterfaceFilesService")
        _interface_files_service = InterfaceFilesService()
    return _interface_files_service
