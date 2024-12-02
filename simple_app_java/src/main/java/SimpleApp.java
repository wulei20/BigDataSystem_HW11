import java.util.Arrays;
import java.util.regex.Pattern;

import scala.Tuple2;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.StorageLevels;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;


public final class SimpleApp {
  private static final Pattern SPACE = Pattern.compile(" ");

  public static void main(String[] args) throws Exception {

    // Create the context with a 60 second batch size
    SparkConf sparkConf = new SparkConf().setAppName("JavaHDFSWordCount");
    JavaStreamingContext ssc = new JavaStreamingContext(sparkConf, Durations.seconds(60));


//    Create the FileInputDStream on the directory and use the stream to count words in new files created

    JavaDStream<String> lines = ssc.textFileStream("hdfs://intro00:8020/user/2020123456/stream"); // you should change path to your own directory on hdfs

    JavaDStream<String> words = lines.flatMap(x -> Arrays.asList(SPACE.split(x)).iterator());
    JavaPairDStream<String, Integer> wordCounts = words.mapToPair(s -> new Tuple2<>(s, 1))
            .reduceByKey((i1, i2) -> i1 + i2);

    wordCounts.print();
    ssc.start();
    ssc.awaitTermination();
  }
}
