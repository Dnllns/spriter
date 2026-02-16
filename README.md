# Spriter: Advanced Sprite Repository & Simulator

[![CI](https://github.com/dnllns/spriter/actions/workflows/ci.yml/badge.svg)](https://github.com/dnllns/spriter/actions/workflows/ci.yml)
[![Docs](https://github.com/dnllns/spriter/actions/workflows/docs.yml/badge.svg)](https://dnllns.github.io/spriter)
[![Release](https://img.shields.io/github/v/release/dnllns/spriter)](https://github.com/dnllns/spriter/releases)
[![License](https://img.shields.io/github/license/dnllns/spriter)](LICENSE)

An advanced system for sprite management, simulation, and analysis, built with **Clean Architecture** and **Python 3.11+**.

## Features

- **Sprite Management**: Upload, categorize, and tag sprites.
- **Simulation**: Run physics-based simulations on sprite entities.
- **Analysis**: Analyze sprite properties and interactions.
- **Documentation**: Comprehensive documentation and API reference.

## Documentation

Full documentation is available at [https://dnllns.github.io/spriter/](https://dnllns.github.io/spriter/).

## Development

This project uses modern Python tooling:

- **Ruff**: For linting and formatting.
- **Pytest**: For testing.
- **Sphinx**: For documentation.
- **GitHub Actions**: For CI/CD.

### Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

### Building Docs

```bash
cd docs
make html
```
