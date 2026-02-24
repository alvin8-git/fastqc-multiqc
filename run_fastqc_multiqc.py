__version__ = "1.0.0"

import argparse
import subprocess
import glob
import os
import sys
import concurrent.futures

VERBOSE = False
QUIET = False

def log(msg):
    if not QUIET and VERBOSE:
        print(msg)
    elif not QUIET and not VERBOSE:
        pass
    elif QUIET:
        pass

def main():
    global VERBOSE, QUIET

    parser = argparse.ArgumentParser(
        description='Run FastQC and MultiQC on paired-end FASTQ files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /data/input --output-dir /data/output --parallel 8
  %(prog)s /data --dry-run --verbose
        """
    )
    parser.add_argument('input_dir', type=str, help='Input directory containing FASTQ files')
    parser.add_argument('--container-input-dir', type=str, default='/input',
                      help='Input directory inside container (default: /input)')
    parser.add_argument('--output-dir', type=str, default=None,
                      help='Output directory for results (default: input directory)')
    parser.add_argument('--fastqc-threads', type=int, default=1,
                      help='Number of threads per FastQC process (default: 1)')
    parser.add_argument('--parallel', type=int, default=1,
                      help='Number of parallel FastQC processes (default: 1)')
    parser.add_argument('-v', '--verbose', action='store_true',
                      help='Enable verbose output')
    parser.add_argument('-q', '--quiet', action='store_true',
                      help='Suppress all output except errors')
    parser.add_argument('--dry-run', action='store_true',
                      help='Show what would be processed without running FastQC')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()

    VERBOSE = args.verbose
    QUIET = args.quiet

    if args.quiet and args.verbose:
        print("Error: Cannot use both --quiet and --verbose", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir if args.output_dir else args.input_dir
    container_input_dir = args.container_input_dir

    if not os.path.isdir(args.input_dir):
        raise ValueError(f"Input directory {args.input_dir} does not exist")

    os.makedirs(output_dir, exist_ok=True)

    patterns = ['*_1.fq.gz', '*_2.fq.gz']
    fastq_files = []
    for pattern in patterns:
        host_files = glob.glob(os.path.join(args.input_dir, pattern))
        container_files = [os.path.join(container_input_dir,
                         os.path.basename(f)) for f in host_files]
        fastq_files.extend(container_files)

    if not fastq_files:
        raise ValueError("No FASTQ files found matching patterns *_1.fq.gz and *_2.fq.gz")

    log(f"Found {len(fastq_files)} FASTQ files")
    log(f"Input directory: {args.input_dir}")
    log(f"Output directory: {output_dir}")
    log(f"Parallel processes: {args.parallel}")
    log(f"Threads per FastQC: {args.fastqc_threads}")

    if args.dry_run:
        print("Dry run - would process the following files:")
        for f in fastq_files:
            print(f"  - {os.path.basename(f)}")
        print(f"\nTotal: {len(fastq_files)} files")
        return

    fastqc_output = os.path.join(output_dir, 'fastqc_results')
    multiqc_output = os.path.join(output_dir, 'multiqc_report')
    os.makedirs(fastqc_output, exist_ok=True)

    commands = []
    for fastq in fastq_files:
        cmd = [
            'fastqc',
            fastq,
            '--outdir', fastqc_output,
            '--threads', str(args.fastqc_threads)
        ]
        commands.append(cmd)

    log("Running FastQC...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [executor.submit(subprocess.run, cmd, check=True) for cmd in commands]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except subprocess.CalledProcessError as e:
                print(f"FastQC failed: {e}", file=sys.stderr)
                raise

    log("Running MultiQC...")
    subprocess.run([
        'multiqc',
        fastqc_output,
        '-o', multiqc_output
    ], check=True)

    log("Done!")

if __name__ == '__main__':
    main()

