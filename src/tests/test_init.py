# src/tests/test_init.py
import pytest
from pathlib import Path
import shutil
import yaml
from typer.testing import CliRunner
from unittest.mock import Mock, patch

from ..commands.init import ProjectInitializer, CloudProvider, ProjectTemplate
from ..utils.errors import ProjectExistsError, ProjectInitError

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing"""
    yield tmp_path
    # Cleanup after tests
    if tmp_path.exists():
        shutil.rmtree(tmp_path)

@pytest.fixture
def project_initializer(temp_dir):
    """Create a ProjectInitializer instance"""
    return ProjectInitializer(
        name="test-project",
        path=temp_dir,
        registry="test-registry",
        provider=CloudProvider.AWS,
        template=ProjectTemplate.BASIC,
        git_init=True,
    )

class TestProjectInitializer:
    def test_project_creation(self, project_initializer, temp_dir):
        """Test basic project creation"""
        project_initializer.initialize()
        
        # Check if project directory exists
        project_dir = temp_dir / "test-project"
        assert project_dir.exists()
        
        # Check if main directories were created
        assert (project_dir / "agents").exists()
        assert (project_dir / "infrastructure").exists()
        assert (project_dir / "scripts").exists()
        
        # Check if config file exists and is valid
        config_file = project_dir / "aiswarm.yaml"
        assert config_file.exists()
        
        with open(config_file) as f:
            config = yaml.safe_load(f)
            assert config["project"]["name"] == "test-project"
            assert config["registry"]["url"] == "test-registry"
            assert config["infrastructure"]["provider"] == "aws"

    def test_existing_project_detection(self, project_initializer, temp_dir):
        """Test detection of existing projects"""
        # Create a fake existing project
        project_dir = temp_dir / "test-project"
        project_dir.mkdir()
        (project_dir / "aiswarm.yaml").touch()
        
        with pytest.raises(ProjectExistsError):
            project_initializer.validate_project_location()

    def test_nested_project_prevention(self, project_initializer, temp_dir):
        """Test prevention of nested projects"""
        # Create a parent project
        parent_dir = temp_dir / "parent-project"
        parent_dir.mkdir()
        (parent_dir / "aiswarm.yaml").touch()
        
        # Try to create a project inside the parent
        nested_initializer = ProjectInitializer(
            name="nested-project",
            path=parent_dir,
            registry="test-registry",
        )
        
        with pytest.raises(ProjectExistsError):
            nested_initializer.validate_project_location()

    def test_example_agent_creation(self, project_initializer, temp_dir):
        """Test example agent creation"""
        project_initializer.initialize()
        
        agent_dir = temp_dir / "test-project" / "agents" / "example-agent"
        assert agent_dir.exists()
        assert (agent_dir / "main.py").exists()
        assert (agent_dir / "Dockerfile").exists()
        assert (agent_dir / "requirements.txt").exists()
        
        # Check if main.py contains required endpoints
        with open(agent_dir / "main.py") as f:
            content = f.read()
            assert "@app.post(\"/execute\")" in content
            assert "@app.get(\"/health\")" in content

    def test_docker_compose_creation(self, project_initializer, temp_dir):
        """Test docker-compose.yml creation"""
        project_initializer.initialize()
        
        compose_file = temp_dir / "test-project" / "docker-compose.yml"
        assert compose_file.exists()
        
        with open(compose_file) as f:
            content = f.read()
            assert "example-agent:" in content
            assert "redis:" in content
            assert "prometheus:" in content

    @patch('git.Repo.init')
    def test_git_initialization(self, mock_git_init, project_initializer, temp_dir):
        """Test git initialization"""
        project_initializer.initialize()
        
        mock_git_init.assert_called_once()
        assert (temp_dir / "test-project" / ".gitignore").exists()

    def test_permission_error_handling(self, temp_dir):
        """Test handling of permission errors"""
        # Mock a permission error
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = PermissionError()
            
            initializer = ProjectInitializer(
                name="test-project",
                path=temp_dir,
            )
            
            with pytest.raises(ProjectInitError):
                initializer.validate_project_location()

    @pytest.mark.parametrize("provider", list(CloudProvider))
    def test_different_providers(self, provider, temp_dir):
        """Test project creation with different cloud providers"""
        initializer = ProjectInitializer(
            name="test-project",
            path=temp_dir,
            provider=provider,
        )
        initializer.initialize()
        
        config_file = temp_dir / "test-project" / "aiswarm.yaml"
        with open(config_file) as f:
            config = yaml.safe_load(f)
            assert config["infrastructure"]["provider"] == provider.value

    def test_force_flag(self, project_initializer, temp_dir):
        """Test force flag behavior"""
        # Create existing directory with content
        project_dir = temp_dir / "test-project"
        project_dir.mkdir()
        (project_dir / "existing-file.txt").touch()
        
        # Should raise error without force
        with pytest.raises(ProjectExistsError):
            project_initializer.validate_project_location()
        
        # Should succeed with force
        forced_initializer = ProjectInitializer(
            name="test-project",
            path=temp_dir,
            force=True,
        )
        forced_initializer.initialize()
        assert project_dir.exists()

# CLI Integration Tests
def test_cli_init_command():
    """Test the CLI init command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            ["init", "test-project", "--registry", "test-registry"]
        )
        assert result.exit_code == 0
        assert "Successfully created project: test-project" in result.output

def test_cli_init_command_with_options():
    """Test CLI init command with various options"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            [
                "init",
                "test-project",
                "--registry", "test-registry",
                "--provider", "aws",
                "--template", "basic",
                "--no-git",
            ]
        )
        assert result.exit_code == 0
        
        # Check if project was created correctly
        config_file = Path("test-project/aiswarm.yaml")
        assert config_file.exists()
        
        with open(config_file) as f:
            config = yaml.safe_load(f)
            assert config["infrastructure"]["provider"] == "aws"
            assert config["project"]["template"] == "basic"