LOCAL_DIR=/storeData/samba/alvin/Docker_Projects/fastqc_multiqc/test_data

# Create output directory with proper permissions
sudo mkdir -p $(pwd)/analysis_results
sudo chown -R $(id -u):$(id -g) $(pwd)/analysis_results
sudo chmod -R 775 $(pwd)/analysis_results

docker run -it \
--user $(id -u):$(id -g) \
-v "${LOCAL_DIR}":/input:ro \
-v $(pwd)/analysis_results:/output \
alvin8/fastqc-multiqc \
/input \
--output-dir /output \
--fastqc-threads 2 \
--parallel 5
