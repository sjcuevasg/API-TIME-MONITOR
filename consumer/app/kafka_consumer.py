
# Kafka Consumer para escuchar los mensajes enviados al topic "api_logs" 
from kafka import KafkaConsumer
#lo usamos para convertir el mensaje recibido de bytes a un diccionario de python
import json
#importamos la funcion save_api_log para guardar el log recibido en la base de datos
from services.logger_service import save_api_log
import os
import time
KAFKA_BROKER= os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
#se conecta al broker de Kafka en la dirección "kafka:9092" y se suscribe al topic "api_logs"
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    #la función value_deserializer se encarga de convertir el mensaje recibido de bytes a un 
    # diccionario de python utilizando json.loads, x representa
    #x representa el mensaje recibido en bytes, se decodifica a utf-8 
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id=KAFKA_GROUP_ID
)

#inicia el loop del consumidor para escuchar los mensajes entrantes en el topic "api_logs".
    #cada vez que se recibe un mensaje, se llama a la función save_api_log para guardar el log en la base de datos
    # pasando el valor del mensaje (que es el log) como argumento
def start_consumer():
    #kafka se demora en reconectarse al broker si este se cae, por lo que se implementa un loop infinito 
    # con manejo de excepciones para reintentar la conexión cada 5 segundos en caso de error
    while True:
        try:
            for message in consumer:
                save_api_log(message.value)
        except Exception as e:
            print(f"Error: {e}. Reintentando en 5s...")
            time.sleep(5)