from database import SessionLocal
from models import ApiLog
#funcion para guardar un log en la base de datos, recibe un diccionario con los datos del log, crea una instancia de ApiLog con esos datos ,
# agrega el log a la sesión de la base de datos, hace commit para guardar los cambios y cierra la sesión
def save_api_log(data: dict):
    db = SessionLocal()
    log = ApiLog(**data)
    db.add(log)
    db.commit()
    db.close()
