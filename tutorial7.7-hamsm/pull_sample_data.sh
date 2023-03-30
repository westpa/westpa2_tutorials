#!/bin/bash

DATA_URL="https://zenodo.org/record/6471213/files/sample_data.tar.gz"

echo "Downloading sample data from Zenodo ... "
wget --continue $DATA_URL

echo "Untarring - this may take a LONG time (~1h on the workstation it was developed on), because of the large number of small files."
echo "Final extracted size will be about ~2.7G, though the footprint on disk may be larger (due to many small files)."
tar -xzf sample_data.tar.gz
