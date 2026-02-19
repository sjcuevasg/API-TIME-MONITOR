#importamos KafkaProducer para enviar mensajes a Kafka y json para serializar los mensajes
from kafka import KafkaProducer
import json
import os
#se conecta al broker de Kafka en la dirección "kafka:9092" y se configura para serializar los mensajes a JSON antes de enviarlos
KAFKA_BROKER= os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    #la función value_serializer se encarga de convertir el mensaje a JSON y luego a bytes para enviarlo a Kafka
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

#funcion encargada de mandar un evento (log) al topic "api_logs" de Kafka, recibe un diccionario con los datos del log
#  y  lo envía utilizando el productor configurado previamente
def publish_event(event: dict):
    producer.send(KAFKA_TOPIC, event)
