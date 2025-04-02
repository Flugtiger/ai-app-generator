# AI Application Generator

## Project Summary

This project is a tool for automatically generating a complete application with a Domain-Driven Design (DDD) model and application services from requirements and commands. It leverages Large Language Models (LLMs) to interpret natural language requirements and generate clean, well-structured code that follows DDD and onion architecture principles.

### Key Features

- **Model Generation**: Convert natural language requirements into a complete domain model with entities, value objects, aggregates, and repositories
- **Application Services Generation**: Create application services based on commands that interact with the domain model
- **Infrastructure Code Generation**: Generate the infrastructure layer based on the domain model and 'infrastructure requirements'
- **Interface Generation**: Generate an interface for the application (currently restricted to a CLI)
- **Project Files Generation**: Generate the project files, e.g. README, third-party dependencies, etc.
- **Command-Line Interface**: Easy-to-use CLI for all operations

### How It Works

1. **Requirements Collection**: Users define model requirements, commands and infrastructure requirements in natural language
2. **App Generation**: The system uses LLMs to interpret requirements and generate a the different application layers (onion architecture)
3. **Code Output**: Generated code is written to the file system in the proper structure

### Milestones

- [x] The ai-app-generator can generate itself from natural language requirements (CLI only)
- [ ] The generated application can be built incrementally by adding and modifying requirements
- [ ] Go beyond CLI applications, i.e. serverless
- [ ] Build a SaaS for generating applications from requirements
- [ ] Build a comprehensive requirements engineering SaaS that provides the base for generating applications using AI

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
python -m src.interface.cli.main model-requirement create --text "A model requirement"
```

### Creating Commands

Create a command using the CLI:

```bash
python -m src.interface.cli.main command create --name MyFirstCommand --description "A command description"
```

### Creating Infrastructure Requirements

Create am infrastructure requirement using the CLI:

```bash
python -m src.interface.cli.main infrastructure-requirement create --text "An infra requirement"
```

### Generating the Application Layers

First, generate a domain model from all model requirements:

```bash
python -m src.interface.cli.main generate model
```

Then, generate the application layer based on commands and the domain model:

```bash
python -m src.interface.cli.main generate application
```

Then, generate the infrastructure layer based on the domain model and the infrastructure requirements:

```bash
python -m src.interface.cli.main generate infrastructure
```

Then, generate the CLI for the application:

```bash
python -m src.interface.cli.main generate interface
```

Lastly, generate the project files:

```bash
python -m src.interface.cli.main generate project
```

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
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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

- `src/application`: Contains application services
- `src/model`: Contains the domain model
- `src/infrastructure`: Contains infrastructure implementations
- `src/interface`: Command-line interface
- `requirements`: Sample requirements and commands

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
