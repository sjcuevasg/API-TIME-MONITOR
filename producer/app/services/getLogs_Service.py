from database import SessionLocal
from models import ApiLog
#funcion para guardar un log en la base de datos, recibe un diccionario con los datos del log, crea una instancia de ApiLog con esos datos ,
# agrega el log a la sesión de la base de datos, hace commit para guardar los cambios y cierra la sesión
def get_api_log():
    db = SessionLocal()
    logs = db.query(ApiLog).order_by(ApiLog.timestamp.desc()).all()
    db.close()
    return logs

