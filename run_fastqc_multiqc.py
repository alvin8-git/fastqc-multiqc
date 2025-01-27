import argparse
import subprocess
import glob
import os
import concurrent.futures

def main():
    parser = argparse.ArgumentParser(description='Run FastQC and MultiQC on paired-end FASTQ files.')
    parser.add_argument('input_dir', type=str, help='Input directory containing FASTQ files')
    parser.add_argument('--output-dir', type=str, default=None, 
                      help='Output directory for results (default: input directory)')
    parser.add_argument('--fastqc-threads', type=int, default=1,
                      help='Number of threads per FastQC process (default: 1)')
    parser.add_argument('--parallel', type=int, default=1,
                      help='Number of parallel FastQC processes (default: 1)')
    
    args = parser.parse_args()

    # Set output directory
    output_dir = args.output_dir if args.output_dir else args.input_dir
    input_dir = args.input_dir

    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory {input_dir} does not exist")
    os.makedirs(output_dir, exist_ok=True)

    # Find FASTQ files
    patterns = ['*_1.fq.gz', '*_2.fq.gz']
    fastq_files = []
    for pattern in patterns:
        fastq_files.extend(glob.glob(os.path.join(input_dir, pattern)))
    
    if not fastq_files:
        raise ValueError("No FASTQ files found matching patterns *_1.fq.gz and *_2.fq.gz")

    # Setup output directories
    fastqc_output = os.path.join(output_dir, 'fastqc_results')
    multiqc_output = os.path.join(output_dir, 'multiqc_report')
    os.makedirs(fastqc_output, exist_ok=True)

    # Generate FastQC commands
    commands = []
    for fastq in fastq_files:
        cmd = [
            'fastqc', 
            fastq, 
            '--outdir', fastqc_output,
            '--threads', str(args.fastqc_threads)
        ]
        commands.append(cmd)

    # Run FastQC in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [executor.submit(subprocess.run, cmd, check=True) for cmd in commands]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except subprocess.CalledProcessError as e:
                print(f"FastQC failed: {e}")
                raise

    # Run MultiQC
    subprocess.run([
        'multiqc',
        fastqc_output,
        '-o', multiqc_output
    ], check=True)

if __name__ == '__main__':
    main()

