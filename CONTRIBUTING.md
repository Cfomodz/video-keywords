# Contributing to vidIQ Python API

Thank you for your interest in contributing to the vidIQ Python API! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/vidiq-python-api.git
   cd vidiq-python-api
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -e .[dev]
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.7 or higher
- Git
- A vidIQ account and API token for testing

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/vidiq-python-api.git
cd vidiq-python-api

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vidiq_api

# Run specific test file
pytest tests/test_vidiq_api.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code with black
black vidiq_api/ tests/

# Lint with flake8
flake8 vidiq_api/ tests/

# Type checking with mypy
mypy vidiq_api/
```

## 📝 Coding Standards

### Code Style
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters (Black default)
- Use meaningful variable and function names

### Type Hints
- All public functions must have type hints
- Use `typing` module for complex types
- Example:
  ```python
  from typing import Dict, List, Optional
  
  def analyze_keyword(self, keyword: str, delay: float = 1.0) -> Dict[str, Any]:
      pass
  ```

### Documentation
- All public functions must have docstrings
- Use Google-style docstrings
- Include parameter types, return types, and examples
- Example:
  ```python
  def analyze_keyword(self, keyword: str, delay: float = 1.0) -> Dict[str, Any]:
      """Analyze a single keyword using vidIQ API.
      
      Args:
          keyword: The keyword to analyze
          delay: Delay in seconds before making the request
          
      Returns:
          Dictionary containing keyword analysis data
          
      Raises:
          ValueError: If keyword is empty
          Exception: If API call fails
          
      Example:
          >>> api = VidiqAPI("token")
          >>> result = api.analyze_keyword("youtube SEO")
          >>> print(result['data']['volume'])
      """
  ```

## 🧪 Testing

### Test Structure
- Tests are located in the `tests/` directory
- Use pytest for testing framework
- Mock external API calls using `unittest.mock`
- Aim for >90% code coverage

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch
from vidiq_api import VidiqAPI

def test_analyze_keyword_success():
    """Test successful keyword analysis"""
    # Test implementation
    pass
```

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API interactions (with mocking)
- **Error Tests**: Test error handling and edge cases

## 🔄 Pull Request Process

### Before Submitting
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** with clear, focused commits
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Run the full test suite**:
   ```bash
   pytest
   flake8 vidiq_api/ tests/
   mypy vidiq_api/
   ```

### Pull Request Guidelines
- **Title**: Clear, descriptive title
- **Description**: Explain what changes you made and why
- **Tests**: Include tests for new features
- **Documentation**: Update README or docs if needed
- **Changelog**: Add entry to CHANGELOG.md

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
```

## 🐛 Bug Reports

### Before Reporting
1. **Search existing issues** to avoid duplicates
2. **Test with latest version**
3. **Gather debugging information**

### Bug Report Template
```markdown
**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.0]
- Package version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

## 💡 Feature Requests

### Before Requesting
1. **Check existing issues** for similar requests
2. **Consider the scope** - does it fit the project goals?
3. **Think about implementation** - how would it work?

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Any other context or screenshots.
```

## 📚 Documentation

### Types of Documentation
- **README**: Overview and quick start
- **API Reference**: Detailed function documentation
- **Examples**: Real-world usage examples
- **Contributing**: This file

### Documentation Standards
- Clear, concise language
- Include code examples
- Keep examples up-to-date
- Use proper markdown formatting

## 🏷️ Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. GitHub Actions will automatically publish to PyPI

## 🤝 Community

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the [Python Community Code of Conduct](https://www.python.org/psf/conduct/)

### Getting Help
- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to vidIQ Python API! 🎉
