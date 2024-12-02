from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext(appName="Py_HDFSWordCount")
ssc = StreamingContext(sc, 60)

lines = ssc.textFileStream("hdfs://intro00:8020/user/[username]/stream")  #  you should change path to your own directory on hdfs
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda x: (x, 1)).reduceByKey(lambda a, b: a+b)
counts.pprint()
ssc.start()
ssc.awaitTermination()


