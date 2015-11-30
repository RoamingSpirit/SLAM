max=9
for g  in `seq 1 $max`
do
	for h  in `seq 1 $max`
	do
		echo "g = 0.$g and h = 0.$h"
		python ../breezyslam/main.py 0.$g 0.$h
		echo "$(($g * 9 + $h - 9)) of 81 Test done." 
	done
done
