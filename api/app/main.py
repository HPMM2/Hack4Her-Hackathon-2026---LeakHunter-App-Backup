from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.tiendas import router as tiendas_router

app = FastAPI(
    title="API de Gestión de Riesgo",
    description="Backend para análisis de riesgo de tiendas con integración Gemini.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tiendas_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "api"}
