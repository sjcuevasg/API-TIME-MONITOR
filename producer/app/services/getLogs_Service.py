from database import SessionLocal
from sqlalchemy import func
from models import ApiLog
#funcion para guardar un log en la base de datos, recibe un diccionario con los datos del log, crea una instancia de ApiLog con esos datos ,
# agrega el log a la sesión de la base de datos, hace commit para guardar los cambios y cierra la sesión
def get_api_log():
    db = SessionLocal()
    logs = db.query(ApiLog).order_by(ApiLog.timestamp.desc()).all()
    db.close()
    return logs

def get_endpoint_stats():
    db = SessionLocal()
    
    # total de visitas por endpoint
    stats = db.query(
        ApiLog.endpoint,
        ApiLog.method,
        func.count(ApiLog.id).label("total_visitas"),
        func.avg(ApiLog.response_time).label("promedio_ms"),
        func.hour(ApiLog.timestamp).label("hora")
    ).group_by(
        ApiLog.endpoint,
        ApiLog.method,
        func.hour(ApiLog.timestamp)
    ).order_by(
        ApiLog.endpoint,
        func.hour(ApiLog.timestamp)
    ).all()
    
    db.close()
    
    # convertir a lista de diccionarios
    return [
        {
            "endpoint": row.endpoint,
            "method": row.method,
            "total_visitas": row.total_visitas,
            "promedio_ms": round(row.promedio_ms, 2),
            "hora": f"{row.hora:02d}:00"
        }
        for row in stats
    ]