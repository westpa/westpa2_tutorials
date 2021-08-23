#!/bin/bash
my_list=(03 05 14 20 24 28 30 35 41 42 50 51 55 56 69 72 74 76 83 85)
for i in ${my_list[@]}; do
	echo "basis_${i} 0.05 basis_${i}_eq2.ncrst" >> bstates.txt
done
