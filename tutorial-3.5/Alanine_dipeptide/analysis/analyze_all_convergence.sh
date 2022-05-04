#!/bin/bash

for i in {0..7}
do
	cd cell_$i
	for j in 2 4 6 8 10 20 30 40 50 60 70 80 90 100
	do
		if [ $j -ne 100 ]
                then
                        cp analysis.py analysis_$j.py
                        sed -i "s/w.niters/$j/g" analysis_$j.py
                        sed -i "s/weights.txt/weights_$j.txt/g" analysis_$j.py
                        sed -i "s/trajectories.pkl/trajectories_$j.pkl/g" analysis_$j.py
                        sed -i "s/trajectories_pruned.pkl/trajectories_pruned_$j.pkl/g" analysis_$j.py
                        sed -i "s/crossings.pkl/crossings_$j.pkl/g" analysis_$j.py
                        python analysis_$j.py
                fi

                if [ $j -eq 100 ]
                then
                        python analysis.py
                fi

	done
	cd ..
done

