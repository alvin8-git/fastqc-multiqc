.PHONY: build test install lint clean help

help:
	@echo "Available targets:"
	@echo "  build   - Build Docker image"
	@echo "  test    - Run test with Docker"
	@echo "  install - Install Python dependencies"
	@echo "  lint    - Run pylint"
	@echo "  clean   - Clean output directories"

build:
	docker build -t alvin8/fastqc-multiqc .

test:
	cd test && ./docker2.sh

install:
	pip3 install -r requirements.txt

lint:
	pylint run_fastqc_multiqc.py

clean:
	rm -rf */results */*_results */*/multiqc_data */*/fastqc_report
