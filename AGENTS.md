# AGENTS.md - Agentic Coding Guidelines for fastqc-multiqc

## Project Overview

This is a Docker-based bioinformatics pipeline that runs FastQC and MultiQC on paired-end FASTQ files in parallel. The main entry point is `run_fastqc_multiqc.py`.

## Build, Run, and Test Commands

### Building the Docker Image

```bash
docker build -t alvin8/fastqc-multiqc .
```

### Running the Pipeline

```bash
# Basic usage
docker run -v /path/to/input:/input -v /path/to/output:/output \
  alvin8/fastqc-multiqc /input --output-dir /output

# With parallel processing
docker run -v /path/to/data:/data \
  alvin8/fastqc-multiqc /data --output-dir /data/results --parallel 8 --fastqc-threads 2
```

### Running Locally (without Docker)

```bash
apt-get install fastqc python3 python3-pip
pip3 install multiqc
python3 run_fastqc_multiqc.py /path/to/input --output-dir /path/to/output --parallel 4
```

### Testing

**No formal test framework (pytest/unittest) in this project.**

Manual test using included test data:
```bash
cd test && ./docker2.sh
```

With pytest (if added):
```bash
pytest tests/test_specific.py::test_function_name -v
```

### Linting

**No linting tools configured.** To add:
```bash
pip3 install pylint && pylint run_fastqc_multiqc.py
```

## Code Style Guidelines

### General Principles

- Write clean, readable code suitable for a bioinformatics production pipeline
- This is a small, single-script project - keep it simple and maintainable
- Prioritize correctness and clarity over clever optimizations

### Imports

- Standard library imports first, then third-party
- Use explicit imports (avoid `from module import *`)
- Group imports: stdlib, third-party, local

```python
# Correct order:
import argparse
import os
import subprocess

import concurrent.futures  # third-party
```

### Formatting

- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Add spaces around operators: `a + b`, not `a+b`
- Use descriptive variable names

### Types

- Python 3.8+ type hints are optional but encouraged for new functions
- Use clear type annotations when functions have complex parameters

### Naming Conventions

- `snake_case` for functions and variables
- `PascalCase` for classes (if any)
- CONSTANTS in UPPER_SNAKE_CASE
- Descriptive names: `output_directory` not `out_dir`

### Error Handling

- Use specific exceptions: `ValueError`, `FileNotFoundError`
- Provide informative error messages
- Fail fast on invalid inputs (validate early)

### Code Structure

- Keep functions focused and small (under 50 lines when possible)
- Add docstrings to public functions
- Use constants for magic numbers

### Docker Best Practices

- Keep Docker images small (use specific base images)
- Run as non-root user in containers
- Use proper volume mounts with `:ro` for read-only inputs

### Git Conventions

- Use meaningful commit messages
- Commit related changes together
- No secrets or credentials in code

## Project File Structure

```
.
├── AGENTS.md                 # This file
├── Dockerfile                # Container definition
├── README.md                 # Project documentation
├── run_fastqc_multiqc.py     # Main Python script
├── test/
│   └── docker2.sh           # Test script
└── test_data/               # Test FASTQ files
```

## Adding Tests

If you want to add tests, use pytest:

1. Create `tests/` directory with `__init__.py`
2. Add test files: `test_pipeline.py`
3. Install test dependencies: `pip3 install pytest pytest-mock`

Example test structure:
```python
# tests/test_pipeline.py
import pytest
from run_fastqc_multiqc import main

def test_invalid_input_directory():
    with pytest.raises(ValueError):
        main()  # with invalid args
```

Run tests:
```bash
pytest tests/ -v
```
