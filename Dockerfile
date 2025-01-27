FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    fastqc \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install MultiQC
RUN pip3 install multiqc

# Copy script
COPY run_fastqc_multiqc.py /usr/local/bin/

# Set default working directory
WORKDIR /data

ENTRYPOINT ["python3", "/usr/local/bin/run_fastqc_multiqc.py"]

