
# Kafka Consumer para escuchar los mensajes enviados al topic "api_logs" 
from kafka import KafkaConsumer
#lo usamos para convertir el mensaje recibido de bytes a un diccionario de python
import json
#importamos la funcion save_api_log para guardar el log recibido en la base de datos
from services.logger_service import save_api_log

#se conecta al broker de Kafka en la dirección "kafka:9092" y se suscribe al topic "api_logs"
consumer = KafkaConsumer(
    "api_logs",
    bootstrap_servers="kafka:9092",
    #la función value_deserializer se encarga de convertir el mensaje recibido de bytes a un diccionario de python utilizando json.loads
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

#inicia el loop del consumidor para escuchar los mensajes entrantes en el topic "api_logs".
def start_consumer():
    #cada vez que se recibe un mensaje, se llama a la función save_api_log para guardar el log en la base de datos
    # pasando el valor del mensaje (que es el log) como argumento
    for message in consumer:
        save_api_log(message.value)
