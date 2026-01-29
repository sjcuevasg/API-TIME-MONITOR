from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models, schemas


Base.metadata.create_all(bind=engine)
#inicializa la aplicación FastAPI con el título "API Monitor MVP"
app = FastAPI(title="API Monitor MVP")
#funcion para obtener la sesión de base de datos e inicializarla
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#endpoint de salud para verificar que la API está funcionando
@app.get("/health")
async def health():
    return {"status": "ok"}


#response_model debe seguir el esquema de la clase ApiLogResponse
@app.post("/logs", response_model=schemas.ApiLogResponse)

#recibe un log que debe ser de tipo ApiLogCreate (objeto con los atributos definidos en esa clase)
#recibe una sesión de base de datos inyectada por Depends(get_db)
async def create_log(
    log: schemas.ApiLogCreate,
    db: Session = Depends(get_db)
):
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

    