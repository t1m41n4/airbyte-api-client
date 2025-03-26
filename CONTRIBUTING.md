# Contributing Guidelines

## Getting Started

1. **Install Prerequisites**
```bash
# On Debian/Ubuntu systems
sudo apt update
sudo apt install python3.10 python3.10-dev python3.10-venv python3-pip
# If Python 3.10 is not available, use Python 3.9 or the latest available version:
sudo apt install python3-dev python3-venv python3-pip
```

2. **Setup Development Environment**
```bash
# Clone the repository
git clone https://github.com/t1m41n4/airbyte-api-client.git
cd airbyte-api-client

# Create virtual environment with the latest Python version
# First, check your Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Workflow

### For Features
```bash
git checkout -b feature/your-feature-name
```

### For Fixes
```bash
# For urgent fixes
git checkout -b hotfix/issue-description
# Example: git checkout -b hotfix/fix-connection-timeout

# For non-urgent bugs
git checkout -b fix/issue-description
# Example: git checkout -b fix/improve-error-handling
```

### Fix Guidelines
1. **Hotfix Process**
   - Direct fix to main/production
   - Minimal scope changes
   - Requires immediate review
   - Auto-deploys after merge

2. **Regular Fix Process**
   - Goes through normal review
   - Can include tests
   - Full CI/CD pipeline
   - Release with next version

3. **Fix Commit Messages**
```bash
# For hotfixes
git commit -m "hotfix: brief description of urgent fix

- What was fixed
- Why it was critical
- Impact of the fix"

# For regular fixes
git commit -m "fix: brief description of the fix

- What was fixed
- How it was fixed
- Related issue number"
```

4. **Fix Documentation**
   - Add to CHANGELOG.md under "Fixes"
   - Update relevant documentation
   - Add migration notes if needed

2. **Code Quality Standards**
- Type hints are mandatory
- Tests required for all features (minimum 90% coverage)
- Black formatting with line length 88
- Docstrings follow Google style
- Import sorting with isort
- Flake8 compliance

3. **Testing Requirements**
```bash
# Run test suite
pytest --cov=. --cov-report=html

# Type checking
mypy .

# Format code
black .
isort .

# Lint code
flake8
```

4. **Pre-commit Checks**
```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit manually
pre-commit run --all-files
```

## Pull Request Process

1. **Before Submitting**
- Update documentation
- Add/update tests
- Update CHANGELOG.md
- Run full test suite
- Update requirements if needed

2. **PR Guidelines**
- Clear, descriptive title
- Reference any related issues
- Include before/after screenshots for UI changes
- Update README if needed
- Add notes about breaking changes

3. **Code Review Process**
- All PRs require at least one review
- Address review comments
- Keep commits atomic and well-described
- Squash commits before merging

## Documentation

1. **Code Documentation**
```python
def function_name(param: str) -> bool:
    """Short description of function.

    Extended description of function.

    Args:
        param: Description of param

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
    pass
```

2. **README Updates**
- Keep examples up to date
- Document new features
- Update configuration options

## CI/CD Pipeline

1. **Automated Checks**
- GitHub Actions for automated testing
- SonarCloud for code quality
- Coverage reports
- Type checking
- Linting

2. **Release Process**
- Automated version bumping
- Release notes generation
- Package publishing
- Docker image building

## Project Structure
```
airbyte-api-client/
├── airbyte_manage.py      # Core client implementation
├── daas_service.py        # DaaS implementation
├── monitoring.py          # Monitoring utilities
├── tests/                 # Test files
├── docs/                  # Documentation
├── frontend/             # UI components
└── examples/             # Usage examples
```

## Support

- Open issues for bugs/features
- Join discussions
- Read our [Code of Conduct](CODE_OF_CONDUCT.md)

## License

By contributing, you agree that your contributions will be licensed under the Business Source License 1.1
