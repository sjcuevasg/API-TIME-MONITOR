#mide la duracion de cada solicitud
import time

#importa Request de fastapi, representa la solicitud HTTP entrante

from fastapi import Request , HTTPException
from starlette.responses import JSONResponse
from messaging.kafka_producer import publish_event
from schemas import ApiLogCreate
#rutas que no se deben loguear ni tener en cuenta para medir tiempo de respuesta
EXCLUDED_PATHS = ["/docs", "/redoc", "/openapi.json", "/favicon.ico"]
'''
funcion del middleware para registrar las solicitudes entrantes
recibe la variable request de tipo request, esta se encarga de representar la solicitud HTTP entrante
recibe call_next que es una funcion que procesa la solicitud y devuelve la respuesta 
'''
async def log_requests(request: Request, call_next):
    #si la ruta de la solicitud está en las rutas excluidas, no se loguea ni mide tiempo solo siguie el flujo normal
    if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
        try:
            return await call_next(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
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
            content={"detail": f"Internal Server Error: {str(e)}"},
        )

    #calcula el tiempo que tardo en procesarse la solicitud
    process_time = (time.time() - start_time) * 1000

    #objeto con los datos del log que se guardara en la base de datos, se llena con los datos de la solicitud 
    # y el tiempo de respuesta ademas sigue el esquema definido en ApiLogCreate para asegurar que los datos sean correctos
    try:
        log_data = ApiLogCreate(
            endpoint=request.url.path,
            method=request.method,
            status_code=status_code,
            response_time=process_time 
        )
    except Exception as e:
        print(f"Error creating ApiLogCreate object: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear el log: {str(e)}")
    #pasamos log_data mediante .dict ya que publish_event espera un diccionario y log_data es un objeto 
    # de tipo ApiLogCreate, dict convierte el objeto en un diccionario con sus campos y valores
    publish_event(log_data.dict())
    #devuelve la respuesta procesada
    return response
