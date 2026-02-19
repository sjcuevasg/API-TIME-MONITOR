#mide la duracion de cada solicitud
import time

#importa Request de fastapi, representa la solicitud HTTP entrante

from fastapi import Request , BackgroundTasks
from starlette.responses import JSONResponse
from .messaging.kafka_producer import publish_event
from .schemas import ApiLogCreate
#rutas que no se deben loguear ni tener en cuenta para medir tiempo de respuesta
EXCLUDED_PATHS = ["/docs", "/redoc", "/openapi.json"]
'''
funcion del middleware para registrar las solicitudes entrantes
recibe la variable request de tipo request, esta se encarga de representar la solicitud HTTP entrante
recibe call_next que es una funcion que procesa la solicitud y devuelve la respuesta 
'''
async def log_requests(request: Request, call_next , response_model= ApiLogCreate):
    #si la ruta de la solicitud está en las rutas excluidas, no se loguea ni mide tiempo solo siguie el flujo normal
    if request.url.path in EXCLUDED_PATHS:
        return await call_next(request)
    start_time = time.time()
    #espera que siga el procesamiento de la solicitud, flujo normal
    #si hay un error durante el procesamiento, captura la excepcion y crea una respuesta de error 500 y guarda el log igualmente
    #si no capturamos la excepcion se perderia el logueo de la solicitud en caso de error y se crashearia la app
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        response = JSONResponse(  
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    #calcula el tiempo que tardo en procesarse la solicitud
    process_time = (time.time() - start_time) * 1000

    #objeto con los datos del log que se guardara en la base de datos, se llena con los datos de la solicitud y el tiempo de respuesta
    log_data = {
    "endpoint": request.url.path,
    "method": request.method,
    "status_code": status_code,
    "response_time": process_time 
    }
    publish_event(log_data)
    #devuelve la respuesta procesada
    return response
