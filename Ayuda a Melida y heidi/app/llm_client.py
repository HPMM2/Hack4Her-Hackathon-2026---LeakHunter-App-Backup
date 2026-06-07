import google.generativeai as genai
from app.config import GEMINI_API_KEY

FALLBACK_PUNTOS = [
    "Se recomienda priorizar la renegociación de condiciones con las tiendas en estado crítico para reducir exposición.",
    "Implementar un plan de monitoreo semanal para las tiendas con riesgo medio.",
    "Evaluar la asignación de recursos y promociones en las tiendas de bajo rendimiento para mejorar rotación.",
]


class GeminiClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self._model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel("gemini-2.5-flash")

    async def analizar(self, resumen_tiendas: str) -> list[str]:
        if not self._model:
            return FALLBACK_PUNTOS

        prompt = (
            f"Eres un analista de negocios senior. A continuación recibes un resumen "
            f"de datos de tiendas.\n\nResumen:\n{resumen_tiendas}\n\n"
            f"Genera exactamente 3 puntos clave de análisis y recomendaciones de negocio "
            f"en español. Devuelve SOLO una lista numerada con los 3 puntos, "
            f"sin introducción ni conclusión."
        )

        try:
            response = await self._model.generate_content_async(prompt)
            texto = response.text
            lineas = [l.strip() for l in texto.split("\n") if l.strip()]
            puntos = []
            for l in lineas:
                limpia = l.lstrip("1234567890.-)• ").strip()
                if limpia:
                    puntos.append(limpia)
            return puntos[:3] if puntos else FALLBACK_PUNTOS
        except Exception:
            return FALLBACK_PUNTOS

    def generar_sumario(self, tiendas_data: list[dict]) -> str:
        if not tiendas_data:
            return "No hay datos de tiendas disponibles."

        total = len(tiendas_data)
        criticas = sum(
            1 for t in tiendas_data
            if t["riskLevel"].strip().lower() in ("crítico", "critico")
        )
        medias = sum(
            1 for t in tiendas_data
            if t["riskLevel"].strip().lower() == "medio"
        )
        riesgo_prom = sum(t["riskPercentage"] for t in tiendas_data) / total

        return (
            f"Total de tiendas: {total}\n"
            f"Críticas: {criticas}\n"
            f"En estado medio: {medias}\n"
            f"Riesgo promedio: {riesgo_prom:.2f}%\n"
        )
