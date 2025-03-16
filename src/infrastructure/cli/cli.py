import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError

from src.application.command_service import (
    CommandCommands,
    CreateCommandInput,
    CreateCommandOutput,
)
from src.application.model_generator_service import (
    GenerateModelInput,
    ModelGeneratorCommands,
)
from src.application.model_requirement_service import (
    CreateModelRequirementInput,
    ModelRequirementCommands,
)
from src.infrastructure.repositories.command.command_file_repository import (
    CommandFileRepository,
)
from src.infrastructure.repositories.model_requirement.model_requirement_file_repository import (
    ModelRequirementFileRepository,
)
from src.model.command.command import Command
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.infrastructure.llm.langchain_llm_service import LangchainLlmService
from src.model.services.llm_service import LlmService
from src.model.services.model_generator import ModelGenerator


class CliError(Exception):
    """Exception raised for CLI errors."""
    pass


def load_json_file(file_path: str) -> Dict:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON content as a dictionary
        
    Raises:
        CliError: If the file cannot be read or parsed
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise CliError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise CliError(f"Invalid JSON in file: {file_path}")


def save_json_file(file_path: str, data: Union[Dict, List, BaseModel]) -> None:
    """
    Save data to a JSON file.
    
    Args:
        file_path: Path to the JSON file
        data: Data to save (dictionary, list, or Pydantic model)
        
    Raises:
        CliError: If the file cannot be written
    """
    try:
        # Create directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert Pydantic model to dict if needed
        if isinstance(data, BaseModel):
            data = data.dict()
            
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise CliError(f"Failed to save file {file_path}: {str(e)}")




class CommandLineInterface:
    """
    Command-line interface for the application.
    """
    
    def __init__(self):
        """Initialize the CLI with repositories and application services."""
        # Initialize repositories
        self.model_requirement_repository = ModelRequirementFileRepository()
        self.command_repository = CommandFileRepository()
        
        # Initialize the last ID based on existing requirements
        existing_requirements = self.model_requirement_repository.get_all()
        ModelRequirement.initialize_last_id(existing_requirements)
        existing_commands = self.command_repository.get_all()
        Command.initialize_last_id(existing_commands)
        
        # Initialize application services
        self.model_requirement_commands = ModelRequirementCommands(
            self.model_requirement_repository
        )
        self.command_commands = CommandCommands(
            self.command_repository
        )
        
        # Initialize model generator with Langchain LLM service
        llm_service = LangchainLlmService()
        model_generator = ModelGenerator(llm_service)
        
        self.model_generator_commands = ModelGeneratorCommands(
            self.model_requirement_repository,
            model_generator
        )
        
        # Set up argument parser
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser for the CLI.
        
        Returns:
            Configured argument parser
        """
        parser = argparse.ArgumentParser(
            description="Domain-Driven Design (DDD) Model Generator CLI"
        )
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        
        # Create command
        create_cmd_parser = subparsers.add_parser(
            "create-command", 
            help="Create a new command"
        )
        create_cmd_parser.add_argument(
            "--input-file", 
            type=str, 
            help="Path to JSON file with input data"
        )
        create_cmd_parser.add_argument(
            "--name", 
            type=str, 
            help="Name of the command"
        )
        create_cmd_parser.add_argument(
            "--description", 
            type=str, 
            help="Description of the command"
        )
        
        # Create model requirement command
        create_req_parser = subparsers.add_parser(
            "create-model-requirement", 
            help="Create a new model requirement"
        )
        create_req_parser.add_argument(
            "--input-file", 
            type=str, 
            help="Path to JSON file with input data"
        )
        create_req_parser.add_argument(
            "--requirement-text", 
            type=str, 
            help="Text of the requirement"
        )
        
        # Generate model command
        gen_model_parser = subparsers.add_parser(
            "generate-model", 
            help="Generate a domain model from requirements"
        )
        gen_model_parser.add_argument(
            "--input-file", 
            type=str, 
            help="Path to JSON file with input data (optional, uses all requirements if not provided)"
        )
        gen_model_parser.add_argument(
            "--output-dir", 
            type=str, 
            default="generated_models", 
            help="Directory to save generated model files"
        )
        
        return parser
    
    def run(self, args=None) -> int:
        """
        Run the CLI with the given arguments.
        
        Args:
            args: Command-line arguments (defaults to sys.argv[1:])
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        if args is None:
            args = self.parser.parse_args()
        else:
            args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return 1
        
        try:
            # Dispatch to the appropriate command handler
            if args.command == "create-command":
                return self._handle_create_command(args)
            elif args.command == "create-model-requirement":
                return self._handle_create_model_requirement(args)
            elif args.command == "generate-model":
                return self._handle_generate_model(args)
            else:
                print(f"Unknown command: {args.command}")
                return 1
        except CliError as e:
            print(f"Error: {str(e)}")
            return 1
        except ValidationError as e:
            print(f"Validation error: {str(e)}")
            return 1
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return 1
    
    def _handle_create_command(self, args) -> int:
        """
        Handle the create-command command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success)
        """
        if args.input_file:
            input_data = load_json_file(args.input_file)
            input_model = CreateCommandInput(**input_data)
        elif args.name and args.description:
            input_model = CreateCommandInput(
                name=args.name,
                description=args.description
            )
        else:
            raise CliError("Either --input-file or both --name and --description must be provided")
        
        result = self.command_commands.create_command(input_model)
        print(f"Created command: {result.json(indent=2)}")
        return 0
    
    def _handle_create_model_requirement(self, args) -> int:
        """
        Handle the create-model-requirement command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success)
        """
        if args.input_file:
            input_data = load_json_file(args.input_file)
            input_model = CreateModelRequirementInput(**input_data)
        elif args.requirement_text:
            input_model = CreateModelRequirementInput(
                requirement_text=args.requirement_text
            )
        else:
            raise CliError("Either --input-file or --requirement-text must be provided")
        
        result = self.model_requirement_commands.create_model_requirement(input_model)
        print(f"Created model requirement: {result.json(indent=2)}")
        return 0
    
    def _handle_generate_model(self, args) -> int:
        """
        Handle the generate-model command.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code (0 for success)
        """
        
        result = self.model_generator_commands.generate_model(GenerateModelInput())
        
        # Save generated files to output directory
        output_dir = args.output_dir
        for file_path, content in result.files.items():
            full_path = Path(output_dir) / file_path
            
            # Create directory if it doesn't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save content as plain text
            with open(full_path, 'w') as f:
                f.write(content)
        
        print(f"Generated model files saved to {output_dir}/")
        return 0


def main():
    """Main entry point for the CLI."""
    cli = CommandLineInterface()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
