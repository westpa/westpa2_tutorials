#!/bin/bash

for i in {0..7}
do
	cd cell_$i
	python analysis.py
	cd ..
done

