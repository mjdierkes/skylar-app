# iOS Project Generator

A Flask-based service that automates the creation of iOS SwiftUI projects with CI/CD integration.

## Features

- Generates modern SwiftUI-based iOS projects
- Configures XcodeGen for project generation
- Sets up Codemagic CI/CD pipeline
- Creates GitHub repository automatically
- Implements best practices for iOS development

## Prerequisites

- Python 3.8+
- Git
- XcodeGen
- GitHub account
- Codemagic account

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ios-project-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export GITHUB_TOKEN="your-github-token"
export CODEMAGIC_API_TOKEN="your-codemagic-token"
```

## Usage

1. Start the server:
```bash
python run.py
```

2. Create a new project:
```bash
curl -X POST http://localhost:5000/create_project \
  -H "Content-Type: application/json" \
  -d '{"project_name": "MyAwesomeApp"}'
```

## Project Structure

```
app/
├── __init__.py
├── config.py
├── exceptions.py
├── project_creator.py
└── services/
    ├── github_service.py
    ├── codemagic_service.py
    ├── project_service.py
    └── templates/
        ├── xcodegen_template.py
        ├── codemagic_template.py
        └── swiftui_template.py
```

## Configuration

The service can be configured through environment variables:

- `GITHUB_TOKEN`: GitHub personal access token
- `CODEMAGIC_API_TOKEN`: Codemagic API token
- `WORKSPACE_DIR`: Directory for project generation (default: ~/workspace)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 