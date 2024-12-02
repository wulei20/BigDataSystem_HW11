from __future__ import print_function
import os
import getpass
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# 创建SparkContext和StreamingContext
sc = SparkContext(appName="Py_HDFSWordCount")
ssc = StreamingContext(sc, 60)

# 检查用户名并设置HDFS路径
username = getpass.getuser()
hdfs_path = f"hdfs://intro00:8020/user/{username}/stream"
print("hdfs_path: ", hdfs_path)

# 设置检查点，用于保存状态以支持状态更新
ssc.checkpoint(f"hdfs://intro00:8020/user/{username}/checkpoint")

# 读取数据流
lines = ssc.textFileStream(hdfs_path)

# 定义一个更新函数，用于累计每个单词的频率
def update_function(new_values, running_count):
    return sum(new_values) + (running_count or 0)

# 每批次统计当前批次词频
word_counts = lines.flatMap(lambda line: line.split(" ")) \
                   .map(lambda word: (word, 1))

# 使用updateStateByKey实现累积
cumulative_word_counts = word_counts.updateStateByKey(update_function)
cnt = 0
# 排序并获取前100个频繁词
def get_top_words(rdd):
    if rdd.isEmpty():
        return
    
    sorted_words = rdd.sortBy(lambda x: -x[1])  # 按频率降序排序
    top_100 = sorted_words.take(100)  # 获取前100个
    print("\nTop 100 Words:")
    for word, count in top_100:
        print(f"{word} {count}")
    output_dir = "./output_files"  # 设置本地存储目录
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在则创建
    global cnt
    output_path = os.path.join(output_dir, f"top_100_words_batch_{cnt}.txt")
    with open(output_path, "w") as f:
        for word, count in top_100:
            f.write(f"{word} {count}\n")
    print(f"Top 100 words for batch {cnt} saved to {output_path}")
    cnt += 1

# 每次处理结果时获取前100个频繁词
cumulative_word_counts.foreachRDD(get_top_words)

# 启动流处理
ssc.start()
ssc.awaitTermination()
