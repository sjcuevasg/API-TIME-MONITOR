from kafka_consumer  import start_consumer
from database import engine
from models import Base
import time
def create_tables():
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            print("Tablas creadas exitosamente")
            break
        except Exception as e:
            print(f"MySQL no disponible, reintentando en 5s... {e}")
            time.sleep(5)


if __name__ == "__main__":
    create_tables()
    start_consumer()
    