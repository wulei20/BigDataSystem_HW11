/* SimpleApp.scala */
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.SparkContext._
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._

object SimpleApp
{
	def main(args: Array[String])
	{
		val sparkConf = new SparkConf().setAppName("ScalaHDFSWordCount")
		// Create the context
		val ssc = new StreamingContext(sparkConf, Seconds(60))

		// Create the FileInputDStream on the directory and use the
		// stream to count words in new files created

		val lines = ssc.textFileStream("hdfs://intro00:8020/user/2020123456/stream") // you should change path to your own directory on hdfs

		val words = lines.flatMap(_.split(" "))
		val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
		wordCounts.print()
		ssc.start()
		ssc.awaitTermination()
	}
}
