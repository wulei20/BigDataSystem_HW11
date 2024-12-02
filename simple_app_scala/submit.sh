APP=./target/simple-project-1.0.jar
CLASS=SimpleApp
spark-submit --name simple_app --verbose --conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:log4j.properties" --class $CLASS  --master local[2]  --executor-memory 2G --total-executor-cores 2 $APP
