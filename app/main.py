from fastapi import FastAPI

app = FastAPI(
    title="API Monitor app",
    description="Sistema de monitoreo de APIs",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "API funcionando correctamente"
    }
