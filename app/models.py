from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base
'''
creamos la clase ApiLog que sirve como modelo de base de datos para almacenar los logs de la API
hereda de la clase Base definida en database.py
al llamar base.metadata.create_all(bind=engine) en main.py, se crea la tabla "api_logs" en la base de datos si no existe 
y se crea toda tabla que herede de Base
'''
class ApiLog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String(255))
    method = Column(String(10))
    status_code = Column(Integer)
    response_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
