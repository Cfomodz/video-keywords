# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-25

### Added
- Initial release of vidIQ Python API wrapper
- `VidiqAPI` class for keyword analysis
- Support for single keyword analysis via `analyze_keyword()`
- Support for batch keyword analysis via `analyze_multiple_keywords()`
- Case-insensitive keyword matching
- Built-in rate limiting with configurable delays
- Comprehensive error handling
- Command line interface
- Type hints for better IDE support
- Full test suite with pytest
- GitHub Actions CI/CD pipeline
- PyPI package distribution

### Features
- **Simple API**: Easy-to-use single class interface
- **Rate Limiting**: Automatic delays to respect API limits
- **Error Handling**: Comprehensive error messages and exception handling
- **Batch Processing**: Analyze multiple keywords efficiently
- **Case Insensitive**: Works with any keyword capitalization
- **Type Safety**: Full type annotations
- **CLI Support**: Command line interface for quick analysis

### Dependencies
- `requests>=2.25.0` - HTTP library for API calls
- `Python>=3.7` - Minimum Python version support

### Documentation
- Comprehensive README with examples
- API reference documentation
- Integration examples for common use cases
- Performance tips and best practices

## [Unreleased]

### Planned
- Async support for high-volume processing
- Caching layer for repeated requests
- Additional keyword metrics
- Export functionality (CSV, JSON)
- Web dashboard interface
