# src/aiswarm/main.py
import typer
from typing import Optional
from pathlib import Path
import sys
from rich.console import Console

from .commands.init import register_init_command
from .commands.build import register_build_command
from .commands.deploy import register_deploy_command
from .commands.agent import register_agent_commands
from .commands.registry import register_registry_commands
from .utils.logger import setup_logging
from .utils.errors import SwarmError

# Initialize console for rich output
console = Console()

# Create main app
app = typer.Typer(
    name="aiswarm",
    help="AI Swarm - Deploy and manage AI agent swarms",
    add_completion=False,
)

def version_callback(value: bool):
    if value:
        console.print("AI Swarm CLI v0.1.0")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version information",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose logging",
    ),
):
    """
    AI Swarm CLI - Deploy and manage AI agent swarms
    """
    # Setup logging
    setup_logging(verbose)

def init_cli():
    """Initialize CLI with all commands"""
    try:
        # Register all command groups
        register_init_command(app)
        register_build_command(app)
        register_deploy_command(app)
        register_agent_commands(app)
        register_registry_commands(app)

        # Add additional command groups here
        
    except Exception as e:
        console.print(f"Failed to initialize CLI: {str(e)}", style="red bold")
        sys.exit(1)

# Error handling for the entire CLI
@app.exception_handler(SwarmError)
def handle_swarm_error(error: SwarmError):
    """Handle custom swarm errors"""
    console.print(f"\nError: {str(error)}", style="red bold")
    raise typer.Exit(1)

@app.exception_handler(Exception)
def handle_exception(error: Exception):
    """Handle unexpected errors"""
    console.print(f"\nUnexpected error: {str(error)}", style="red bold")
    if "--verbose" in sys.argv:
        console.print_exception()
    raise typer.Exit(1)

# Context settings for better help messages
app.pretty_exceptions_enable = False
app.pretty_exceptions_show_locals = False

def cli():
    """Entry point for the CLI"""
    init_cli()
    app()

if __name__ == "__main__":
    cli()