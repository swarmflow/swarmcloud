# AI Swarm CLI

A collaborative platform for building and managing AI agent swarms. This project enables teams to develop, share, and deploy AI agents across cloud providers.

## 🤝 Getting Started as a Contributor

```bash
# Clone repository
git clone https://github.com/swarmflow/swarmcloud
cd swarmcloud

# Run the setup script - this creates your development environment
python setup.py

# Activate your development environment
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

That's it! You're ready to start developing.

## 🏗️ Project Structure

```
swarmcloud
├── src/
|   ├── main.py          # CLI entry point
│   │── sdk/           # Agent development SDK
│   │── commands/      # CLI commands
│   │── core/         # Core functionality
|   ├── utils/
|   ├── templates/
│   └── tests/             # Test suite
├── examples/              # Examples
├── docs/                  # Documentation
├── setup.py              # Development setup script
└── pyproject.toml        # Project dependencies
```

## 🧑‍💻 Development Workflow

1. **Start a New Feature**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Create or Modify an Agent**
   ```bash
   # Create new agent
   aiswarm agent create my-agent
   
   # Agent code is in:
   agents/my-agent/agent.py
   ```

3. **Test Your Changes**
   ```bash
   # Run test suite
   pytest src/tests/
   
   # Test specific agent
   aiswarm agent test my-agent
   ```

4. **Submit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/your-feature-name
   ```

## 🔨 Common Development Tasks

### Building Agents
```python
# agents/my-agent/agent.py
from aiswarm.sdk.agent import BaseAgent

class MyAgent(BaseAgent):
    """Your agent implementation"""
    async def execute(self, input_data):
        return {"result": await self.process(input_data)}
```

### Running the Test Suite
```bash
# All tests
pytest

# Specific test file
pytest src/tests/test_agents.py

# With coverage
pytest --cov=aiswarm
```

### Code Quality
All checks run automatically on commit, but you can run manually:
```bash
# Format code
black src/
isort src/

# Lint
flake8 src/
```

## 🤖 Using Prebuilt Agents

Access the shared agent repository:
```bash
# List available agents
aiswarm registry list

# Use a prebuilt agent
aiswarm agent use text-processor

# Publish your agent
aiswarm registry publish my-agent --visibility public
```

## 👥 Team Collaboration

### Agent Registry
- Public agents are available to everyone
- Private agents require authentication
- Use tags to version your agents

### Shared Development
```bash
# Update your environment
git pull
python setup.py

# Create feature branch
git checkout -b feature/new-feature

# Push changes
git push origin feature/new-feature
```

### Code Review Process
1. Create PR with description of changes
2. Automated tests must pass
3. Request review from team members
4. Address feedback
5. Merge when approved

## 🐛 Troubleshooting

### Environment Issues
```bash
# Reset development environment
rm -rf .venv
python setup.py

# Update dependencies
pip install -e .
```

### Common Problems

1. **Tests Failing**
   - Ensure virtual environment is active
   - Update dependencies
   - Check test logs

2. **Agent Build Issues**
   - Verify Docker is running
   - Check agent configuration
   - Review build logs

3. **Development Environment**
   - Use `python --version` to verify Python 3.9.18
   - Ensure virtual environment is active
   - Check `.env` file exists

## 📚 Resources

- **Documentation**: Project documentation is in `docs/`
- **Examples**: Check `agents/examples/` for reference implementations
- **Tests**: Look at `src/tests/` for usage examples

## 🤝 Contributing Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use type hints
   - Add docstrings
   - Keep functions focused

2. **Testing**
   - Write tests for new features
   - Maintain test coverage
   - Use meaningful assertions

3. **Commits**
   - Use conventional commits
   - Keep changes focused
   - Reference issues

4. **Documentation**
   - Update README if needed
   - Add docstrings
   - Comment complex logic

## 🆘 Getting Help

- **Issues**: Use GitHub Issues for bugs
- **Questions**: Use GitHub Discussions
- **Security**: See SECURITY.md
- **Chat**: Join our Discord

Remember:
- Always work in your virtual environment
- Pull before starting new work
- Run tests before committing
- Ask for help when stuck!

## 📄 License

MIT License - see LICENSE file for details.