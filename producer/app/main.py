from fastapi import FastAPI, Depends, Request, HTTPException

#importa el middleware de logueo de solicitudes
from middleware import log_requests

from services.getLogs_Service import get_api_log
#inicializa la aplicación FastAPI con el título "API Monitor MVP"
app = FastAPI(title="API Monitor MVP")
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Monitor MVP")

# agrega esto justo después de crear el app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
registra el middleware de logueo de solicitudes en la aplicación FastAPI
basicamente le dice a fastapi que use el middleware log_requests para cada solicitud HTTP entrante
'''
@app.middleware("http")
async def middleware(request: Request, call_next):
    #para cada peticion entrante, llama a la funcion log_requests definida en middleware.py y devuelve su resultado
    return await log_requests(request, call_next)



#endpoint de salud para verificar que la API está funcionando
@app.get("/health", tags=["HEALTH"], status_code=200)
async def health():
    return {"status": "ok"}


@app.get("/logs", tags=["LOGS"], status_code=200,
 responses={
    200: {"description": "Logs obtenidos exitosamente"},
    404: {"description": "No hay logs registrados"},
    500: {"description": "Error interno del servidor"}
})
async def get_logs():
    try:
        logs = get_api_log()
        if not logs:
            raise HTTPException(status_code=404, detail="No hay logs registrados")
        return logs
    except HTTPException:
        raise  # deja pasar las HTTPException que lanzamos nosotros
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {str(e)}")



















#response_model debe seguir el esquema de la clase ApiLogResponse
'''
    Este metodo es unicamente para crear un log en la base de datos de manera manual
    no es utilizado en produccion ya que el logueo se hace automaticamente con el middleware
    ya que solo guardaria logs creados manualmente al hacer un post a /logs

@app.post("/logs", response_model=schemas.ApiLogResponse)
#recibe un log que debe ser de tipo ApiLogCreate (objeto con los atributos definidos en esa clase)
#recibe una sesión de base de datos inyectada por Depends(get_db)
async def create_log(   log: schemas.ApiLogCreate,    db: Session = Depends(get_db)):
    #define el objeto db_log de tipo ApiLog (modelo de base de datos)
    db_log = models.ApiLog(
        #recibe parametros del log recibido en la petición
        endpoint=log.endpoint,
        method=log.method,
        status_code=log.status_code,
        response_time=log.response_time
    )
    #ejecuta las operaciones de base de datos para agregar, confirmar y refrescar el log
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log


'''