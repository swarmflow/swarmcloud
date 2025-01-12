# src/aiswarm/commands/build.py
def register_build_command(app: typer.Typer):
    build_app = typer.Typer(name="build", help="Build agent images")
    app.add_typer(build_app)

    @build_app.command("all")
    def build_all(
        tag: str = typer.Option("latest", help="Tag for built images"),
        push: bool = typer.Option(False, help="Push images after building"),
    ):
        """Build all agents in the project"""
        # Add build logic here
        pass

# src/aiswarm/commands/deploy.py
def register_deploy_command(app: typer.Typer):
    deploy_app = typer.Typer(name="deploy", help="Deploy swarm")
    app.add_typer(deploy_app)

    @deploy_app.command()
    def deploy(
        env: str = typer.Option("dev", help="Environment to deploy to"),
        dry_run: bool = typer.Option(False, help="Perform a dry run"),
    ):
        """Deploy the swarm"""
        # Add deployment logic here
        pass

# src/aiswarm/commands/agent.py
def register_agent_commands(app: typer.Typer):
    agent_app = typer.Typer(name="agent", help="Manage agents")
    app.add_typer(agent_app)

    @agent_app.command("create")
    def create_agent(
        name: str = typer.Argument(..., help="Name of the agent"),
        template: str = typer.Option("basic", help="Template to use"),
    ):
        """Create a new agent"""
        # Add agent creation logic here
        pass

    @agent_app.command("list")
    def list_agents():
        """List all agents"""
        # Add agent listing logic here
        pass

# src/aiswarm/commands/registry.py
def register_registry_commands(app: typer.Typer):
    registry_app = typer.Typer(name="registry", help="Manage container registry")
    app.add_typer(registry_app)

    @registry_app.command("login")
    def registry_login(
        url: str = typer.Argument(..., help="Registry URL"),
        username: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True, hide_input=True),
    ):
        """Login to container registry"""
        # Add registry login logic here
        pass