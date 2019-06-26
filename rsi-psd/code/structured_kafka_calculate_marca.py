#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Consumes messages from one or more topics in Kafka and does wordcount.
 Usage: structured_kafka_wordcount.py <bootstrap-servers> <subscribe-type> <topics>
   <bootstrap-servers> The Kafka "bootstrap.servers" configuration. A
   comma-separated list of host:port.
   <subscribe-type> There are three kinds of type, i.e. 'assign', 'subscribe',
   'subscribePattern'.
   |- <assign> Specific TopicPartitions to consume. Json string
   |  {"topicA":[0,1],"topicB":[2,4]}.
   |- <subscribe> The topic list to subscribe. A comma-separated list of
   |  topics.
   |- <subscribePattern> The pattern used to subscribe to topic(s).
   |  Java regex string.
   |- Only one of "assign, "subscribe" or "subscribePattern" options can be
   |  specified for Kafka source.
   <topics> Different value format depends on the value of 'subscribe-type'.

 Run the example
    `$ bin/spark-submit examples/src/main/python/sql/streaming/structured_kafka_calculate_probe.py \
    host1:port1,host2:port2 subscribe topic1,topic2`
    
bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3 /home/rsi-psd-vm/Documents/projeto-rsi-psd/code/structured_kafka_calculate_marca.py localhost:9092 subscribe real-time
"""
from __future__ import print_function

import sys
import math

from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import from_json
import paho.mqtt.client as mqtt
import json


THINGSBOARD_HOST = '127.0.0.1'
ACCESS_TOKEN = 'kgbVzwxehHDsHtNGt76N'


def processRow(row):
    print(row)
    # row_data = "{" + row.word + ":" + str(row.count) + "}"
    row_data = { row.MARCA_SHORT : row.__getitem__("count")}
    # Write row to storage
    client = mqtt.Client()
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)
    # Sending humidity and temperature data to ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(row_data), 1)



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: structured_kafka_calculate_marca.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()

    # Create DataSet representing the stream of input lines from kafka
    df = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    fields = [StructField('MAC', StringType(), True), \
    StructField('MARCA', StringType(), True), \
    StructField('SSID', StringType(), True), \
    StructField('MARCA_SHORT', StringType(), True)]
    schema = StructType(fields)

    new_df = df.select(from_json(df.value, schema).alias("pkg")) \
        .select("pkg.MAC", "pkg.MARCA", "pkg.SSID", "pkg.MARCA_SHORT")

    
    df_marca = new_df.select("MAC","MARCA_SHORT").distinct()
    df_marca = df_marca.groupBy("MARCA_SHORT").count()

   
    # Start running the query that prints the running counts to the console
    query = df_marca\
        .writeStream\
        .outputMode('complete')\
        .foreach(processRow)\
        .start()

    query.awaitTermination()