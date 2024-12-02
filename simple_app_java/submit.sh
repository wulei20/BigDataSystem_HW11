APP=./target/simple-project-1.0.jar
CLASS=SimpleApp
spark-submit --name simple_app \
--conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:src/main/resources/log4j.properties" \
--verbose --class $CLASS \
--master local[2] \
--executor-memory 2G \
--total-executor-cores 2 \
$APP

