from pydantic import BaseModel


class DatosTienda(BaseModel):
    id: str
    name: str
    customerId: str
    calmonth: str
    territoryD: str
    comercialSubchannelD: str
    customerSize: str
    coolers: int
    doors: int
    transactions: int
    uniBoxesSoldM: float
    riskPercentage: float
    riskLevel: str
    segment: str


class DetalleRiesgo(BaseModel):
    conteo_critico: int
    conteo_medio: int
    conteo_bajo: int
    resumen_texto_agente: str
    puntos_clave_ia: list[str]


class TiendaParaLista(BaseModel):
    id: str
    name: str
    territoryD: str
    segment: str
    riskPercentage: float
    riskLevel: str


class RespuestaBackendCompleta(BaseModel):
    resumen_riesgo: DetalleRiesgo
    lista_tiendas: list[TiendaParaLista]
