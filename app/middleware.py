#mide la duracion de cada solicitud
import time

#importa Request de fastapi, representa la solicitud HTTP entrante
from fastapi import Request

#importa SessionLocal para manejar las sesiones de la base de datos
from .database import SessionLocal

#importa el modelo ApiLog que representa la tabla de logs en la base de datos
from .models import ApiLog

#rutas que no se deben loguear ni tener en cuenta para medir tiempo de respuesta
EXCLUDED_PATHS = ["/docs", "/redoc", "/openapi.json"]



'''
funcion del middleware para registrar las solicitudes entrantes
recibe la variable request de tipo request, esta se encarga de representar la solicitud HTTP entrante
recibe call_next que es una funcion que procesa la solicitud y devuelve la respuesta 
'''
async def log_requests(request: Request, call_next):
    #si la ruta de la solicitud está en las rutas excluidas, no se loguea ni mide tiempo solo siguie el flujo normal
    if request.url.path in EXCLUDED_PATHS:
    return await call_next(request)


    start_time = time.time()

    
    #espera que siga el procesamiento de la solicitud, flujo normal
    #si hay un error durante el procesamiento, captura la excepcion y crea una respuesta de error 500 y guarda el log igualmente
    #si no capturamos la excepcion se perderia el logueo de la solicitud en caso de error y se crashearia la app
    try:
        response = await call_next(request)
    except Exception as e:
        status_code = 500
        response = JSONResponse(  
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
    #calcula el tiempo que tardo en procesarse la solicitud
    process_time = (time.time() - start_time) * 1000
    #crea sesion de base de datos
    db = SessionLocal()
    #intenta crear un nuevo log en la base de datos
    try:
        log = ApiLog(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time=process_time
        )
        db.add(log)
        db.commit()
    finally:
        db.close()
    #devuelve la respuesta procesada
    return response
