# src/aiswarm/commands/init.py
from pathlib import Path
from typing import Optional, Dict, List
import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
import yaml
import jinja2
import shutil
import json
from enum import Enum
import os
import uuid
from datetime import datetime

from ..core.config import SwarmConfig
from ..utils.logger import get_logger
from ..utils.errors import ProjectInitError, ProjectExistsError, ValidationError

logger = get_logger(__name__)
console = Console()


class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    LOCAL = "local"


class ProjectTemplate(str, Enum):
    BASIC = "basic"
    DISTRIBUTED = "distributed"
    MONITORING = "monitoring"


class ProjectInitializer:
    def __init__(
        self,
        name: str,
        path: Path,
        registry: Optional[str] = None,
        provider: CloudProvider = CloudProvider.AWS,
        template: ProjectTemplate = ProjectTemplate.BASIC,
        git_init: bool = True,
        force: bool = False,
    ):
        self.name = name
        self.base_path = path
        self.project_path = path / name
        self.registry = registry
        self.provider = provider
        self.template = template
        self.git_init = git_init
        self.force = force
        self.project_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat()

    def is_swarm_project(self, path: Path) -> bool:
        """Check if directory is already a swarm project"""
        indicators = [
            "aiswarm.yaml",
            "agents",
            "infrastructure",
        ]
        return any((path / indicator).exists() for indicator in indicators)

    def find_parent_swarm_project(self, path: Path) -> Optional[Path]:
        """Check if any parent directory is a swarm project"""
        current = path
        while current != current.parent:
            if self.is_swarm_project(current):
                return current
            current = current.parent
        return None

    def validate_project_location(self) -> None:
        """Validate the project location"""
        if self.project_path.exists() and any(self.project_path.iterdir()):
            if not self.force:
                if not Confirm.ask(
                    f"\nDirectory {self.project_path.name} already exists and is not empty. Continue?"
                ):
                    raise typer.Abort()

        if self.is_swarm_project(self.project_path):
            raise ProjectExistsError(
                f"Directory {self.project_path} is already a swarm project"
            )

        parent_project = self.find_parent_swarm_project(self.project_path)
        if parent_project:
            raise ProjectExistsError(
                f"Cannot create project inside existing swarm project at {parent_project}"
            )

        try:
            self.project_path.mkdir(parents=True, exist_ok=True)
            test_file = self.project_path / ".write_test"
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            raise ProjectInitError(
                f"No write permission in directory {self.project_path}"
            )

    def create_project_structure(self) -> None:
        """Create the project directory structure"""
        try:
            directories = [
                "agents",
                f"infrastructure/{self.provider}",
                "scripts",
                "config",
                "tests",
                "docs",
            ]

            for dir_path in directories:
                (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)
                (self.project_path / dir_path / ".gitkeep").touch()

        except Exception as e:
            raise ProjectInitError(f"Failed to create project structure: {str(e)}")

    def generate_config(self) -> None:
        """Generate the project configuration files"""
        config = {
            "project": {
                "name": self.name,
                "id": self.project_id,
                "created_at": self.created_at,
                "template": self.template,
            },
            "registry": {"url": self.registry, "type": "docker-registry"},
            "infrastructure": {
                "provider": self.provider,
                "region": "us-east-1",  # Default region
            },
            "agents": [],
            "services": {
                "message_queue": {"type": "redis", "version": "7.0"},
                "monitoring": {"enabled": True, "type": "prometheus"},
            },
        }

        with open(self.project_path / "aiswarm.yaml", "w") as f:
            yaml.safe_dump(config, f, sort_keys=False)

    def create_example_agent(self) -> None:
        """Create an example agent"""
        agent_path = self.project_path / "agents" / "example-agent"
        agent_path.mkdir(exist_ok=True)

        # Create main.py
        main_content = """
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

class Task(BaseModel):
    input: Any
    parameters: Dict[str, Any] = {}

class Response(BaseModel):
    status: str
    result: Any

@app.post("/execute")
async def execute_task(task: Task) -> Response:
    try:
        # Add your agent logic here
        result = task.input  # Echo input for example
        return Response(status="success", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
"""
        with open(agent_path / "main.py", "w") as f:
            f.write(main_content)

        # Create Dockerfile
        dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        with open(agent_path / "Dockerfile", "w") as f:
            f.write(dockerfile_content)

        # Create requirements.txt
        requirements_content = """
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
redis>=4.0.0
prometheus-client>=0.12.0
"""
        with open(agent_path / "requirements.txt", "w") as f:
            f.write(requirements_content)

    def create_docker_compose(self) -> None:
        """Generate docker-compose.yml for local development"""
        compose_content = """
version: '3.8'

services:
  example-agent:
    build: ./agents/example-agent
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
"""
        with open(self.project_path / "docker-compose.yml", "w") as f:
            f.write(compose_content)

    def init_git(self) -> None:
        """Initialize git repository"""
        try:
            import git

            git.Repo.init(self.project_path)

            gitignore_content = """
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
            with open(self.project_path / ".gitignore", "w") as f:
                f.write(gitignore_content)

        except ImportError:
            logger.warning("GitPython not installed. Skipping git initialization.")
        except Exception as e:
            logger.warning(f"Failed to initialize git: {str(e)}")

    def initialize(self) -> None:
        """Main initialization method"""
        try:
            self.validate_project_location()

            with console.status("[bold green]Creating project...") as status:
                status.update("[bold green]Creating directory structure...")
                self.create_project_structure()

                status.update("[bold green]Generating configuration...")
                self.generate_config()

                status.update("[bold green]Creating example agent...")
                self.create_example_agent()

                status.update("[bold green]Creating docker-compose...")
                self.create_docker_compose()

                if self.git_init:
                    status.update("[bold green]Initializing git...")
                    self.init_git()

            console.print(
                f"\n✨ Successfully created project: {self.name}", style="green bold"
            )
            console.print("\nNext steps:")
            console.print(f"1. cd {self.name}")
            console.print("2. Review and update aiswarm.yaml")
            console.print("3. Build your agents: aiswarm build")
            console.print("4. Deploy locally: aiswarm deploy --local")

        except Exception as e:
            console.print(f"\n❌ Error: {str(e)}", style="red bold")
            if self.project_path.exists() and Confirm.ask(
                "Do you want to clean up the created files?"
            ):
                shutil.rmtree(self.project_path)
            raise typer.Exit(1)


def register_init_command(app: typer.Typer) -> None:
    @app.command()
    def init(
        name: str = typer.Argument(..., help="Name of the project"),
        path: Path = typer.Option(
            Path.cwd(),
            help="Path where the project should be created",
            exists=True,
            dir_okay=True,
            writable=True,
        ),
        registry: Optional[str] = typer.Option(
            None,
            help="Container registry URL",
        ),
        provider: CloudProvider = typer.Option(
            CloudProvider.AWS,
            help="Cloud provider for deployment",
        ),
        template: ProjectTemplate = typer.Option(
            ProjectTemplate.BASIC,
            help="Project template to use",
        ),
        no_git: bool = typer.Option(
            False,
            help="Skip git initialization",
        ),
        force: bool = typer.Option(
            False,
            help="Force creation even if directory exists",
        ),
    ):
        """Initialize a new AI Swarm project"""
        initializer = ProjectInitializer(
            name=name,
            path=path,
            registry=registry,
            provider=provider,
            template=template,
            git_init=not no_git,
            force=force,
        )
        initializer.initialize()
