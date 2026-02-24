# TODO.md - Improvements for Download, Install, and Test

## High Priority

### Add requirements.txt
Create `requirements.txt` for easy pip installation:
```
multiqc
pytest
pytest-mock
```

### Add Makefile
Create `Makefile` with common commands:
```makefile
.PHONY: build test install lint clean

build:
	docker build -t alvin8/fastqc-multiqc .

test:
	cd test && ./docker2.sh

install:
	pip3 install -r requirements.txt

lint:
	pylint run_fastqc_multiqc.py

clean:
	rm -rf */results */*_results
```

### Add .dockerignore
```
__pycache__
*.pyc
.git
test_data/
*.md
```

## Medium Priority

### Add GitHub Actions CI
Create `.github/workflows/ci.yml`:
- Build Docker image
- Run linter
- Run tests (if added)

### Add version info to script
```python
__version__ = "1.0.0"
```

### Add setup.py or pyproject.toml
For proper package installation:
```toml
[project]
name = "fastqc-multiqc"
version = "1.0.0"
dependencies = ["multiqc"]
```

## Low Priority

### Add shell completion
Add argparse completion for bash/zsh

### Add verbose/quiet flags
```python
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')
```

### Add dry-run mode
Show what would be processed without running FastQC

### Split into modules
Move functions to separate files for better maintainability:
- `fastqc_multiqc/
  - __init__.py
  - cli.py
  - fastqc.py
  - multiqc.py
```
