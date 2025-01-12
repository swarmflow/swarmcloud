We are in pre-release, join our discord to learn more and contribute https://discord.gg/zBgNDbZnx7

# AI Swarm CLI

A CLI tool for deploying and managing AI agent swarms. Build, deploy, and manage distributed AI agents across different cloud providers.

## Features

- Create and manage AI agent swarms
- Support for multiple cloud providers (AWS, GCP, Azure)
- Local development environment with Docker
- Built-in templates for common agent patterns
- Container registry management
- Infrastructure as Code deployment
- Monitoring and observability

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- Python 3.9.18
- Docker and Docker Compose
- Git

### Optional (for cloud deployments)
- AWS CLI (for AWS deployment)
- Google Cloud SDK (for GCP deployment)
- Azure CLI (for Azure deployment)

### System Dependencies

#### On Ubuntu/Debian
```bash
# Update package list
sudo apt-get update

# Install system dependencies
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    curl

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### On macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install \
    pyenv \
    openssl \
    readline \
    sqlite3 \
    xz \
    zlib \
    docker
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/aiswarm.git
cd aiswarm
```

2. Install pyenv and set Python version:
```bash
# Install pyenv
curl https://pyenv.run | bash

# Add to your shell configuration (~/.bashrc, ~/.zshrc, etc.):
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

# Restart your shell
exec $SHELL

# Install and set Python version
pyenv install 3.9.18
pyenv local 3.9.18
```

3. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. Set up development environment:
```bash
# Setup everything (virtual env, dependencies, pre-commit hooks)
make dev-setup
```

## Development Environment

### Virtual Environment

The project uses Poetry for dependency management and virtual environment control.

```bash
# Activate virtual environment
poetry shell

# Deactivate
exit  # or 'deactivate'

# Run a command in virtual environment without activating
poetry run <command>
```

### Common Development Tasks

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Clean build artifacts
make clean

# Build package
make build
```

## Usage

### Creating a New Project

```bash
# Initialize new project
aiswarm init my-project

# Create with specific provider
aiswarm init my-project --provider aws

# Create with registry
aiswarm init my-project --registry my-registry.azurecr.io
```

### Managing Agents

```bash
# Create new agent
aiswarm agent create text-processor

# List agents
aiswarm agent list

# Build agents
aiswarm build
```

### Deployment

```bash
# Deploy locally
aiswarm deploy --local

# Deploy to cloud
aiswarm deploy --provider aws
```

### Registry Management

```bash
# Login to registry
aiswarm registry login

# Push agent
aiswarm registry push agent-name

# Pull agent
aiswarm registry pull agent-name
```

## Project Structure

```
my-ai-project/
├── agents/                     # Individual agent implementations
│   └── example-agent/         
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
├── infrastructure/            # IaC templates
│   ├── aws/
│   ├── gcp/
│   └── azure/
├── scripts/                   # Utility scripts
├── tests/                     # Project tests
├── .env.example              # Environment variables template
├── docker-compose.yml        # Local development setup
└── aiswarm.yaml             # Project configuration
```

## Configuration

### aiswarm.yaml
```yaml
project:
  name: my-project
  version: "1.0.0"

registry:
  url: my-registry.azurecr.io
  type: azure

infrastructure:
  provider: aws
  region: us-east-1

agents:
  - name: text-processor
    replicas: 3
    resources:
      cpu: 1
      memory: "2G"
```

## Troubleshooting

### Common Issues

1. **Poetry installation fails**
   - Ensure Python 3.9+ is installed
   - Try installing with pip: `pip install --user poetry`
   - Check system dependencies

2. **Docker issues**
   - Ensure Docker daemon is running
   - Check permissions: `sudo usermod -aG docker $USER`
   - Restart Docker service

3. **Virtual Environment Problems**
   - Delete .venv and reinstall: `rm -rf .venv && make dev-setup`
   - Check Poetry configuration: `poetry config --list`

4. **Build Failures**
   - Check Docker has sufficient resources
   - Verify registry credentials
   - Check network connectivity

### Getting Help

If you encounter issues:

1. Check the troubleshooting guide above
2. Review logs: `aiswarm logs`
3. Enable debug mode: `aiswarm --debug <command>`
4. Open an issue on GitHub

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Use pre-commit hooks

### Testing

```bash
# Run all tests
make test

# Run specific test file
pytest src/tests/test_init.py

# Run with coverage
make test-cov
```

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: [Project Issues](https://github.com/your-username/aiswarm/issues)
- Documentation: [Project Wiki](https://github.com/your-username/aiswarm/wiki)
- Community: [Discord Server](https://discord.gg/zBgNDbZnx)