# AMPEL360 Coding Standards

## General Principles

### Code Quality
- All code must be readable, maintainable, and well-documented
- Follow the principle of least surprise
- Write code that tells a story
- Prefer composition over inheritance
- Use meaningful names for variables, functions, and classes

### Documentation Standards
- All public functions and classes must have docstrings
- Use clear, concise comments for complex logic
- Maintain up-to-date README files for all modules
- Document API changes and breaking changes

## Language-Specific Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Maximum line length: 88 characters (Black formatter standard)
- Use f-strings for string formatting
- Prefer pathlib over os.path for file operations

```python
# Example: Good Python code structure
from pathlib import Path
from typing import Dict, List, Optional

def optimize_qnnn(
    constraints_path: Path,
    passenger_range: tuple[int, int] = (150, 220)
) -> Dict[str, Any]:
    """Optimize passenger capacity using QAOA algorithm.
    
    Args:
        constraints_path: Path to constraints YAML file
        passenger_range: Min and max passenger capacity
        
    Returns:
        Dictionary containing optimization results
        
    Raises:
        FileNotFoundError: If constraints file doesn't exist
    """
    # Implementation here
    pass
```

### YAML Configuration Files
- Use lowercase with hyphens for keys
- Indent with 2 spaces
- Use quotes only when necessary
- Maintain consistent structure across files

```yaml
# Example: Good YAML structure
configuration:
  metadata:
    version: "5.0"
    created-date: "2025-08-26"
  
  optimization-parameters:
    qnnn-range:
      min: 150
      max: 220
    risk-factors:
      cvar-alpha: 0.8
      beta: 0.25
```

### JavaScript/TypeScript
- Use ESLint with Airbnb configuration
- Prefer const over let, never use var
- Use async/await over Promises.then()
- Use meaningful destructuring
- Maximum line length: 80 characters

### SQL
- Use uppercase for SQL keywords
- Use lowercase for table and column names
- Always use explicit JOIN syntax
- Include appropriate indexes for performance

## Architecture Standards

### File Organization
```
project/
├── src/                    # Source code
│   ├── core/              # Core business logic
│   ├── utils/             # Utility functions
│   ├── config/            # Configuration files
│   └── tests/             # Test files
├── docs/                  # Documentation
├── scripts/               # Build and deployment scripts
└── requirements/          # Dependency files
```

### Module Structure
- Each module should have a single responsibility
- Use clear public interfaces
- Hide implementation details
- Minimize dependencies between modules

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Fail fast and fail clearly

### Testing Requirements
- Minimum 80% code coverage
- Unit tests for all business logic
- Integration tests for system interfaces
- Performance tests for critical paths

## Security Standards

### Authentication & Authorization
- Use strong authentication mechanisms
- Implement role-based access control
- Never hardcode credentials
- Use secure session management

### Data Protection
- Encrypt sensitive data at rest and in transit
- Use parameterized queries to prevent SQL injection
- Validate all inputs
- Implement proper logging without exposing sensitive data

### Code Security
- Regular dependency updates
- Static code analysis
- Secure coding practices
- Regular security reviews

## Performance Standards

### Optimization Guidelines
- Profile before optimizing
- Focus on algorithmic improvements first
- Use appropriate data structures
- Minimize memory allocation in hot paths

### Resource Management
- Close resources properly (files, connections, etc.)
- Use connection pooling for databases
- Implement appropriate caching strategies
- Monitor memory usage

## Review Process

### Code Review Requirements
- All code must be reviewed before merge
- Reviews must cover functionality, style, and security
- Use pull/merge requests for all changes
- Maintain review comments for future reference

### Quality Gates
- All tests must pass
- Code coverage requirements must be met
- Static analysis must pass without errors
- Documentation must be updated

## Tools and Automation

### Required Tools
- Code formatters (Black for Python, Prettier for JS/TS)
- Linters (pylint, ESLint)
- Type checkers (mypy for Python, TypeScript)
- Security scanners (bandit, npm audit)

### CI/CD Integration
- Automated testing on all commits
- Automated code quality checks
- Automated security scanning
- Automated deployment to staging environments

---

**Document Control**
- Version: 1.0
- Effective Date: 2025-08-26
- Review Date: 2026-02-26
- Owner: Chief Architect DT