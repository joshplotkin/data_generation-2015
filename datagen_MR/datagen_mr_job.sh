#python mkdummy.py $1
hadoop fs -rm -r -skipTrash /datagen/trans_fact/

time hadoop jar /usr/phd/3.0.0.0-249/hadoop-mapreduce/hadoop-streaming.jar \
-Dmapred.reduce.tasks=1 \
-input /datagen/dummy_files/* \
-output /datagen/trans_fact \
-file /data2/datagen_MR/EXECUTE.py -mapper EXECUTE.py
echo 3 > /proc/sys/vm/drop_caches

#hadoop fs -cat /datagen/trans_fact/*
hadoop fs -du -s -h /datagen/trans_fact
