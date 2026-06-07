import csv
from app.models import DatosTienda, TiendaParaLista, DetalleRiesgo, RespuestaBackendCompleta
from app.config import CSV_PATH


def load_tiendas_csv(path: str = CSV_PATH) -> list[DatosTienda]:
    tiendas = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tiendas.append(DatosTienda(
                id=row["id"],
                name=row["name"],
                customerId=row["customerId"],
                calmonth=row["calmonth"],
                territoryD=row["territoryD"],
                comercialSubchannelD=row["comercialSubchannelD"],
                customerSize=row["customerSize"],
                coolers=int(row["coolers"]),
                doors=int(row["doors"]),
                transactions=int(row["transactions"]),
                uniBoxesSoldM=float(row["uniBoxesSoldM"]),
                riskPercentage=float(row["riskPercentage"]),
                riskLevel=row["riskLevel"],
                segment=row["segment"],
            ))
    return tiendas


def calcular_conteos_riesgo(tiendas: list[DatosTienda]) -> tuple[int, int, int]:
    critico = 0
    medio = 0
    bajo = 0
    for t in tiendas:
        level = t.riskLevel.strip().lower()
        if level in ("crítico", "critico"):
            critico += 1
        elif level == "medio":
            medio += 1
        elif level == "bajo":
            bajo += 1
    return critico, medio, bajo


def transformar_tiendas(tiendas: list[DatosTienda]) -> list[TiendaParaLista]:
    return [
        TiendaParaLista(
            id=t.id,
            name=t.name,
            territoryD=t.territoryD,
            segment=t.segment,
            riskPercentage=t.riskPercentage,
            riskLevel=t.riskLevel,
        )
        for t in tiendas
    ]


def generar_resumen_texto(total: int, critico: int, medio: int) -> str:
    return f"Vista Todos: {total} tiendas — {critico} críticas y {medio} en estado medio."


def ensamblar_respuesta(tiendas: list[DatosTienda], puntos_ia: list[str]) -> RespuestaBackendCompleta:
    critico, medio, bajo = calcular_conteos_riesgo(tiendas)
    total = len(tiendas)
    resumen = DetalleRiesgo(
        conteo_critico=critico,
        conteo_medio=medio,
        conteo_bajo=bajo,
        resumen_texto_agente=generar_resumen_texto(total, critico, medio),
        puntos_clave_ia=puntos_ia,
    )
    lista = transformar_tiendas(tiendas)
    return RespuestaBackendCompleta(resumen_riesgo=resumen, lista_tiendas=lista)
