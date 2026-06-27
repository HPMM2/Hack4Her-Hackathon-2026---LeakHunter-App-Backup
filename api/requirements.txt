# API — API de Gestión de Riesgo

Backend REST para analizar riesgo de tiendas usando inteligencia artificial (Gemini 2.5 Flash). Desarrollado con FastAPI.

---

## Requisitos previos

### 1. Verificar si ya tienes Python instalado

Abre una terminal (PowerShell, CMD o terminal) y ejecuta:

```bash
python --version
```

- Si ves algo como `Python 3.10.x` o superior → **ya lo tienes, omite el paso 2**.
- Si ves un error o la versión es menor a 3.10 → continúa con el paso 2.

### 2. Instalar Python (solo si no lo tienes)

1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga la **última versión estable** (3.12 o 3.13)
3. Ejecuta el instalador
4. **IMPORTANTE:** Marca la casilla **"Add Python to PATH"** antes de hacer clic en "Install Now"
5. Confirma con: abre una nueva terminal y ejecuta `python --version`

---

## Configuración del proyecto

### 3. Clonar o copiar el proyecto

Ubícate en la carpeta del proyecto:

```bash
cd ruta/del/proyecto/API
```

### 4. Crear un entorno virtual (recomendado)

Esto aísla las dependencias del proyecto del resto del sistema.

```bash
python -m venv venv
```

Actívalo:

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```bash
  venv\Scripts\activate.bat
  ```
- **Mac / Linux:**
  ```bash
  source venv/bin/activate
  ```

Sabrás que funcionó porque verás `(venv)` al inicio de la línea en la terminal.

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Configurar variables de entorno

```bash
cp .env.example .env
```

Abre el archivo `.env` que se acaba de crear y reemplaza los valores:

| Variable | Descripción |
|----------|-------------|
| `GEMINI_API_KEY` | Tu API key de Google Gemini (la obtienes en [aistudio.google.com](https://aistudio.google.com/apikey)) |
| `CSV_PATH` | Ruta al archivo CSV con los datos de tiendas (por defecto `data/tiendas.csv`) |

### 7. Colocar el archivo CSV

Copia tu archivo CSV en la carpeta `data/` del proyecto con el nombre `tiendas.csv`.

El CSV debe contener las siguientes columnas (en cualquier orden):

```
id,name,customerId,calmonth,territoryD,comercialSubchannelD,customerSize,coolers,doors,transactions,uniBoxesSoldM,riskPercentage,riskLevel,segment
```

---

## Ejecutar la API

```bash
python run.py
```

La API se iniciará en `http://localhost:8000`.

---

## Verificar que funciona

### Health check

Abre en tu navegador o ejecuta:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{"status": "ok", "service": "ayuda-a-melida"}
```

### Endpoint principal

```bash
curl -X POST http://localhost:8000/api/tiendas/resumen
```

Respuesta esperada (ejemplo):

```json
{
  "resumen_riesgo": {
    "conteo_critico": 5,
    "conteo_medio": 12,
    "conteo_bajo": 83,
    "resumen_texto_agente": "Vista Todos: 100 tiendas — 5 críticas y 12 en estado medio.",
    "puntos_clave_ia": [
      "Se recomienda priorizar la renegociación...",
      "Implementar un plan de monitoreo semanal...",
      "Evaluar la asignación de recursos..."
    ]
  },
  "lista_tiendas": [...]
}
```

### Documentación interactiva (Swagger)

Abre `http://localhost:8000/docs` en tu navegador.

---

## Estructura del proyecto

```
API/
├── app/
│   ├── __init__.py
│   ├── main.py                  # App FastAPI, CORS, health check
│   ├── config.py                # Variables de entorno
│   ├── models.py                # Modelos Pydantic
│   ├── services.py              # Lógica de negocio
│   ├── llm_client.py            # Cliente Gemini
│   └── endpoints/
│       ├── __init__.py
│       └── tiendas.py           # POST /api/tiendas/resumen
├── data/
│   └── tiendas.csv              # ← Tu archivo CSV aquí
├── .env                         # Variables de entorno (no comitear)
├── .env.example                 # Template del .env
├── run.py                       # Punto de entrada
├── requirements.txt             # Dependencias
└── README.md                    # Esta guía
```

---

## Consumir desde Swift (iOS)

### Configuración previa

Como todo es local, en el `Info.plist` de tu app iOS agrega:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
```

### Modelos Swift

Mapea la respuesta con estos structs:

```swift
struct RespuestaBackendCompleta: Codable {
    let resumenRiesgo: DetalleRiesgo
    let listaTiendas: [TiendaParaLista]
}

struct DetalleRiesgo: Codable {
    let conteoCritico: Int
    let conteoMedio: Int
    let conteoBajo: Int
    let resumenTextoAgente: String
    let puntosClaveIa: [String]
}

struct TiendaParaLista: Codable {
    let id: String
    let name: String
    let territoryD: String
    let segment: String
    let riskPercentage: Double
    let riskLevel: String
}
```

### Llamada al endpoint

```swift
import Foundation

func fetchResumen() async throws -> RespuestaBackendCompleta {
    let url = URL(string: "http://localhost:8000/api/tiendas/resumen")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"

    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(RespuestaBackendCompleta.self, from: data)
}
```

Usa `http://localhost:8000` si corres en el simulador. Para un dispositivo físico, usa la IP local de la máquina (ej. `http://192.168.x.x:8000`).

### Health check

```swift
func checkHealth() async throws -> Bool {
    let url = URL(string: "http://localhost:8000/health")!
    let (_, response) = try await URLSession.shared.data(from: url)
    return (response as? HTTPURLResponse)?.statusCode == 200
}
```

---

## Detener el servidor

Presiona `Ctrl + C` en la terminal donde se está ejecutando.

Para desactivar el entorno virtual (si lo creaste):

```bash
deactivate
```
