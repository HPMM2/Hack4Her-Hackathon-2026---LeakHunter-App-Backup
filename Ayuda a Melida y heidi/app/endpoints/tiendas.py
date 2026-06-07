from fastapi import APIRouter, HTTPException
from app.models import RespuestaBackendCompleta
from app.services import load_tiendas_csv, ensamblar_respuesta
from app.llm_client import GeminiClient
from app.config import CSV_PATH

router = APIRouter(prefix="/api/tiendas", tags=["Tiendas"])
llm = GeminiClient()


@router.post("/resumen", response_model=RespuestaBackendCompleta)
async def resumen_tiendas():
    try:
        tiendas = load_tiendas_csv(CSV_PATH)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Archivo CSV no encontrado en la ruta: {CSV_PATH}. "
                   f"Verifica que el archivo exista y que la variable CSV_PATH en el .env sea correcta.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer el CSV: {str(e)}",
        )

    datos_dict = [t.model_dump() for t in tiendas]
    sumario = llm.generar_sumario(datos_dict)
    puntos_ia = await llm.analizar(sumario)

    return ensamblar_respuesta(tiendas, puntos_ia)
