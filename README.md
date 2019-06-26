# Envio de Dados do Spark Structured Stream para o ThingsBoard via MQTT


O Spark Structured Streaming é um mecanismo de processamento de fluxo de dados construído sobre o mecanismo Spark SQL, capaz de ler grandes fluxos de dados de forma incremental e continuamente atualizar o resultado final a medida que os dados vão chegando. Já o ThingsBoard é uma plataforma aberta de IoT para coleta, processamento e visualização de dados e gerenciamento de dispositivos. Através do uso do protocolo de comunicação MQTT (Message Queueing Telemetry Transport) é possível enviar fluxos de dados estruturados computados no Spark com o uso de uma Dataset/DataFrame API em Scala, Java, Python ou R, para visualização no ThingsBoard. No tutorial a seguir fazemos uma pequena demonstração utilizando o Pyspark(python):

## 	Conexão MQTT:
	
Instalar a biblioteca paho-mqtt.
Definir o ip do host onde no qual irá acessar o thingsboard.
Definir o token do device ao qual será exibido os dados no thingsboard.
Definir uma função que será chamada no “.foreach” e receberá cada linha do data frame para ser enviado ao thingsboard.
Processar a linha do data frame, definindo a chave e resgatando o valor que foi gerado no data frame através do “__getitem__”.
Criar a conexão mqtt.
Setar o token do dispositivo no qual será enviado o dado.
Conectar com o host, setando o ip, a porta e o tempo de checagem entre os dois dispositivos.
Publicar os dados no thingsboard, que por padrão é no endereço 'v1/devices/me/telemetry', os dados terão que ser convertidos para o formato json para ser enviado.







```python
Enviando o data frame para a função.
#Start running the query that prints the running counts to the console
    query = df_count_probe\
        	.writeStream\
        	.outputMode('complete')\
        	.foreach(processRow)\
        	.start()
    query.awaitTermination()

Função para processar data frame e enviar dados para o thingsboard.

def processRow(row):
    print(row)
    # row_data = "{" + row.key + ":" + str(row.count) + "}"
    row_data = { "probe" : row.__getitem__("count")}
    # Write row to storage
    client = mqtt.Client()
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)
    # Sending humidity and temperature data to ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(row_data), 1)
```
