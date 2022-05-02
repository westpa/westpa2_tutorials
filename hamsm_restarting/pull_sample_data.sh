#!/bin/bash

DATA_URL="https://zenodo.org/record/6471213/files/sample_data.tar.gz"

echo "Downloading sample data from Zenodo ... "
wget --continue $DATA_URL

bash untar.sh sample_data.tar.gz
