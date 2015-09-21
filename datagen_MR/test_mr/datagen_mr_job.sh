hadoop jar /usr/phd/3.0.0.0-249/hadoop-mapreduce/hadoop-streaming.jar \
-Dmapred.reduce.tasks=0 \
-Dmapred.mapper.tasks=$1 \
-input /datagen/dummy.txt \
-output /datagen/trans_fact \
-file `pwd`/EXECUTE.py -mapper EXECUTE.py
echo 3 > /proc/sys/vm/drop_caches
