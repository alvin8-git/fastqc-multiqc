# FastQC + MultiQC Parallel Processing Pipeline

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.8%2B-success?logo=python)

A containerized solution for automated quality control analysis of NGS data with parallel processing capabilities.

## Features
- Parallel execution of FastQC analyses
- Automatic MultiQC report generation
- Docker containerization for reproducibility
- Configurable thread/process parameters
- Output directory specification

## Installation

### Docker Installation
```bash
docker pull alvin8/fastqc-multiqc:latest
```

### Local Installation
```bash
git clone https://github.com/alvin8-git/fastqc-multiqc.git
cd fastqc-multiqc
docker build -t alvin8/fastqc-multiqc .
```

## Usage

### Basic Usage
```bash
docker run -v /path/to/input:/input -v /path/to/output:/output \
  alvin8/fastqc-multiqc \
  /input \
  --output-dir /output
```

### Advanced Usage with Parallel Processing
```bash
docker run -v /path/to/data:/data \
  alvin8/fastqc-multiqc \
  /data \
  --output-dir /data/results \
  --parallel 8 \
  --fastqc-threads 2
```

## Parameters

| Parameter           | Description                                  | Default |
|---------------------|----------------------------------------------|---------|
| `input_dir`         | Input directory with FASTQ files             | Required|
| `--output-dir`      | Output directory for results                 | input_dir |
| `--parallel`        | Number of parallel FastQC processes          | 1       |
| `--fastqc-threads`  | Threads per FastQC instance                   | 1       |

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

## Docker Hub
Available on Docker Hub:  
https://hub.docker.com/r/alvin8/fastqc-multiqc

## GitHub Repository
https://github.com/alvin8-git/fastqc-multiqc
