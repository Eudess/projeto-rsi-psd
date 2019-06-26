from kafka import KafkaProducer
import pandas as pd
import time
import json
import sys

def probe_to_json(df, counter):
    dic = dict(df.iloc[counter][1:])
    dic_to_json = json.dumps(dic)
    return dic_to_json

def time_calculate(df, line1, line2, accelerated_time=1 ):
    time_stamp1 = df.iloc[line1][0]
    time_stamp2 = df.iloc[line2][0]
    result = (time_stamp2 - time_stamp1) // accelerated_time

    return result

def start_probe(df, producer, accelerated_time=1):
    line1 = 0
    line2 = 1
    while line1 < df.shape[0]:
        """
        if not (line1 == 0 or line1 == df.shape[0]):
            time_gap = time_calculate(df, line1, line2, accelerated_time)
            try:
                time.sleep(time_gap)
            except:
                print("linha 1: ", line1, "time: ", df.iloc[line1][0])
                print()
                print("linha 2: ", line2, "time: ", df.iloc[line2][0])
        """                
        my_json = probe_to_json(df,line1)
        producer.send("real-time", my_json)
        
        line1 += 1
        line2 += 1

if __name__ == "__main__":

    #sys.argv[1] = "../csv/result.csv"
    try:
        local_csv = sys.argv[1]
    except:
        local_csv = "../csv/result.csv"
    try:
        server_host = sys.argv[2]
    except:
        server_host = "localhost:9092"
    try:
        accelerated_time = int(sys.argv[3])
    except:
        accelerated_time = 1

   
    my_df = pd.read_csv(local_csv, sep=";")
    my_df = my_df.fillna("NoSSID")

    #Create an instance of the kafka producer
    producer = KafkaProducer(bootstrap_servers=server_host, value_serializer=lambda v: str(v).encode("utf-8"))

    start_probe(my_df, producer, accelerated_time=100)