# AI Application Generator

## Project Summary

This project is a tool for automatically generating an application with a Domain-Driven Design (DDD) model and application services from requirements and commands. It leverages Large Language Models (LLMs) to interpret natural language requirements and generate clean, well-structured code that follows DDD principles.

### Key Features

- **Model Generation**: Convert natural language requirements into a complete domain model with entities, value objects, aggregates, and repositories
- **Application Services Generation**: Create application services based on commands that interact with the domain model
- **File Management**: Read and write code to the file system while maintaining proper structure
- **Command-Line Interface**: Easy-to-use CLI for all operations

### How It Works

1. **Requirements Collection**: Users define model requirements in natural language
2. **Command Definition**: Users define commands that represent actions in the system
3. **Model Generation**: The system uses LLMs to interpret requirements and generate a domain model
4. **Application Services Generation**: The system generates application services based on commands and the domain model
5. **Code Output**: Generated code is written to the file system in the proper structure

## Usage Guide

### Installation

```bash
# Clone the repository
git clone git@github.com:Flugtiger/ai-app-generator.git
cd ai-app-generator

# Install dependencies
pip install -e .
```

### Creating Model Requirements

Create a model requirement using the CLI:

```bash
python -m src.infrastructure.cli.cli create-model-requirement --input-file requirements/model/example.json
```

Example requirement JSON:

```json
{
  "requirement_text": "The system needs to manage customers. Each customer has a name, email, and address. Customers can place orders."
}
```

### Creating Commands

Create a command using the CLI:

```bash
python -m src.infrastructure.cli.cli create-command --input-file requirements/application/example.json
```

Example command JSON:

```json
{
  "name": "CreateCustomer",
  "description": "Creates a new customer in the system with the provided details"
}
```

### Generating a Domain Model

Generate a domain model from all requirements:

```bash
python -m src.infrastructure.cli.cli generate-model
```

This will create all the necessary domain model files.

### Generating Application Services

Generate application services based on commands and the domain model:

```bash
python -m src.infrastructure.cli.cli generate-application-services
```

This will create application service files that implement the commands using the domain model.

## Building and Development

### Prerequisites

- Python 3.8 or higher
- Access to an LLM API (currently configured for Anthropic Claude)

### Development Setup

1. Clone the repository:

   ```bash
   git clone git@github.com:Flugtiger/ai-app-generator.git
   cd ai-app-generator
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:

   ```bash
   pip install -e .
   ```

4. Set up your API key:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   # On Windows: set ANTHROPIC_API_KEY=your_api_key_here
   ```

### Running Tests

```bash
pytest
```

### Project Structure

- `src/model`: Contains the domain model
- `src/application`: Contains application services
- `src/infrastructure`: Contains infrastructure implementations
  - `cli`: Command-line interface
  - `llm`: LLM service implementations
  - `repositories`: Repository implementations
- `requirements`: Sample requirements and commands

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
