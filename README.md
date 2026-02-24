# FastQC + MultiQC Parallel Processing Pipeline

[![CI](https://github.com/alvin8-git/fastqc-multiqc/actions/workflows/ci.yml/badge.svg)](https://github.com/alvin8-git/fastqc-multiqc/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
[![Python](https://img.shields.io/badge/Python-3.8%2B-success?logo=python)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A containerized solution for automated quality control analysis of NGS data with parallel processing capabilities.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
  - [Clone Repository](#clone-repository)
  - [Build Docker Image](#build-docker-image)
- [Running the Pipeline](#running-the-pipeline)
  - [Basic Usage](#basic-usage)
  - [Advanced Usage](#advanced-usage)
  - [Command-Line Options](#command-line-options)
- [Demo: Run Test Data](#demo-run-test-data)
- [Input Requirements](#input-requirements)
- [Output Structure](#output-structure)
- [Pushing to GitHub](#pushing-to-github)
- [Contributing](#contributing)
- [License](#license)

## Features

- Parallel execution of FastQC analyses
- Automatic MultiQC report generation
- Docker containerization for reproducibility
- Configurable thread/process parameters
- Dry-run mode for testing
- Verbose and quiet output modes

## Quick Start

```bash
# Clone, build, and run with test data
git clone https://github.com/alvin8-git/fastqc-multiqc.git
cd fastqc-multiqc
docker build -t alvin8/fastqc-multiqc .
docker run -v $(pwd)/test_data:/input:ro -v $(pwd)/output:/output alvin8/fastqc-multiqc /input --output-dir /output
```

## Installation

### Clone Repository

```bash
git clone https://github.com/alvin8-git/fastqc-multiqc.git
cd fastqc-multiqc
```

### Build Docker Image

```bash
docker build -t alvin8/fastqc-multiqc .
```

Or use the Makefile:

```bash
make build
```

## Running the Pipeline

### Basic Usage

```bash
docker run -v /path/to/input:/input:ro -v /path/to/output:/output \
  alvin8/fastqc-multiqc \
  /input \
  --output-dir /output
```

### Advanced Usage

```bash
docker run -v /path/to/data:/data:ro \
  alvin8/fastqc-multiqc \
  /data \
  --output-dir /data/results \
  --parallel 8 \
  --fastqc-threads 2
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_dir` | Input directory with FASTQ files | Required |
| `--output-dir` | Output directory for results | input_dir |
| `--parallel` | Number of parallel FastQC processes | 1 |
| `--fastqc-threads` | Threads per FastQC instance | 1 |
| `-v, --verbose` | Enable verbose output | false |
| `-q, --quiet` | Suppress all output except errors | false |
| `--dry-run` | Show files to process without running | false |
| `--version` | Show version number | - |
| `--help` | Show help message | - |

## Demo: Run Test Data

This repository includes test FASTQ files in `test_data/`.

### Option 1: Using Docker

```bash
# Create output directory
mkdir -p output

# Run with test data
docker run --user $(id -u):$(id -g) \
  -v $(pwd)/test_data:/input:ro \
  -v $(pwd)/output:/output \
  alvin8/fastqc-multiqc /input --output-dir /output --parallel 4
```

### Option 2: Using Make

```bash
make test
```

### Option 3: Dry Run (No Execution)

```bash
docker run --rm alvin8/fastqc-multiqc test_data --dry-run
```

Or locally:

```bash
python3 run_fastqc_multiqc.py test_data --dry-run
```

### Option 4: Local Execution (Without Docker)

```bash
# Install dependencies
pip3 install -r requirements.txt
# or
make install

# Run
python3 run_fastqc_multiqc.py test_data --output-dir output --parallel 4
```

## Input Requirements

- Paired-end FASTQ files named `*_1.fq.gz` and `*_2.fq.gz`
- Minimum Docker memory: 4GB RAM
- Recommended: 1 CPU core per parallel process

## Output Structure

```
output_dir/
├── fastqc_results/
│   ├── sample1_1_fastqc.html
│   ├── sample1_1_fastqc.zip
│   └── ...
└── multiqc_report/
    ├── multiqc_report.html
    └── multiqc_data/
```

## Pushing to GitHub

```bash
# 1. Initialize git (if not already)
git init

# 2. Add remote
git remote add origin https://github.com/alvin8-git/fastqc-multiqc.git

# 3. Create a new branch (optional)
git checkout -b main

# 4. Add and commit changes
git add .
git commit -m "Initial commit"

# 5. Push to GitHub
git push -u origin main
```

### Update Existing Repository

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
