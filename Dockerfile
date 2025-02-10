FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    fastqc \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install MultiQC using pip3
RUN pip3 install multiqc

# Set environment variable to ensure PATH includes /usr/local/bin
ENV PATH="/usr/local/bin:${PATH}"

# Create a non-root user
RUN useradd -ms /bin/bash fastqcuser

# Set working directory and permissions
WORKDIR /app
COPY run_fastqc_multiqc.py /app/

# Set proper permissions
RUN chown -R fastqcuser:fastqcuser /app

# Switch to non-root user
USER fastqcuser

# Copy script
COPY run_fastqc_multiqc.py /usr/local/bin/

# Set default working directory
WORKDIR /data

ENTRYPOINT ["python3", "/usr/local/bin/run_fastqc_multiqc.py"]
