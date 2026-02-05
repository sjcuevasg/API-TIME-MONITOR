from pydantic import BaseModel
from datetime import datetime
'''
creamos una clase ApiLogCreate que define el esquema para crear un nuevo log de API
ayuda a validar los datos de entrada cuando se crea un nuevo log
basemodel es la clase base de pydantic que proporciona funcionalidades de validación y serialización
'''
class ApiLogCreate(BaseModel):
    endpoint: str
    method: str
    status_code: int
    response_time: float
'''
creamos una clase ApiLogResponse que define el esquema para la respuesta al crear o recuperar un log de API
hereda de ApiLogCreate para reutilizar los campos definidos allí
'''
class ApiLogResponse(ApiLogCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
