# API Pagos Web (Espacio Clientes)

**Versión:** 1.0.0

# API Pagos Web (Espacio Clientes)
**Versión:** 1.0.0

## 📖 Descripción
Este proyecto es una API REST construida con FastAPI para el "Espacio Clientes" de Pagos Web. Permite:
- Autenticación vía JWT
- Consulta de deudas de clientes contra base de datos Oracle
- Manejo de pool de conexiones con cx_Oracle
- Validación de datos de entrada con Pydantic
- Configuración de CORS y entornos (desarrollo / producción)

## ✨ Características
- `/token` (POST): Obtiene un token JWT a partir de credenciales
- `/epacio-cliente/consultar-deuda/` (GET): Consulta deudas de un cliente (requiere token)
- Pool de conexiones Oracle configurable
- Soporte para CORS según orígenes definidos
- Documentación automática Swagger y ReDoc

## 🛠 Requisitos
- Python 3.10 o superior
- Oracle Instant Client instalado (para cx_Oracle)
- Git

## 🚀 Instalación
1. Clona este repositorio y accede a la carpeta:
```bash
git clone https://github.com/tu-usuario/ApiPagosWEB.git
cd ApiPagosWEB
Crea y activa un entorno virtual:

bash
python -m venv .venv
Windows (PowerShell):

powershell
.venv\Scripts\Activate
macOS/Linux:

bash
source .venv/bin/activate
Instala las dependencias:

bash
pip install --upgrade pip
pip install -r requirements.txt
⚙️ Configuración
Crea un archivo .env en la raíz del proyecto con:

env
DB_USER=mi_user
DB_PASSWORD=mi_password
DB_HOST=mi_host
DB_SERVICE=OMEGA
ORACLE_POOL_MIN=2
ORACLE_POOL_MAX=10
ORACLE_POOL_INC=1

SECRET_KEY=tu_clave_ultra_larga_y_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ALLOWED_ORIGINS='["http://localhost:8000","http://127.0.0.1:8000"]'
ENVIRONMENT=development
(Opcional) Revisa y ajusta los parámetros de pool en config/settings.py

📁 Estructura del proyecto
text
ApiPagosWEB/
├── api/
│   ├── api.py             # Definición de endpoints y lógica principal
│   ├── auth.py            # Seguridad JWT y utilidades
│   └── models/
│       └── deuda.py       # Esquemas Pydantic para respuesta de deuda
├── config/
│   ├── conexion.py        # Pool de conexiones Oracle
│   └── settings.py        # Carga de variables de entorno
├── requirements.txt       # Lista de dependencias
├── .env                   # Variables de entorno (edítalo)
├── .gitignore
└── prueba.html            # Cliente web de ejemplo para login y consulta
🏃‍♂️ Uso
Inicia la API en modo desarrollo:

bash
uvicorn api.api:app --reload
Accede desde tu navegador:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Obtener token
bash
curl -X POST "http://localhost:8000/token" \
  -d "username=aqpa&password=123456"
Respuesta:

json
{
  "access_token": "<tu_jwt_token>",
  "token_type": "bearer"
}
Consultar deuda
bash
curl -G "http://localhost:8000/epacio-cliente/consultar-deuda/" \
  -H "Authorization: Bearer <tu_jwt_token>" \
  --data-urlencode "nro_documento_cliente=4510123" \
  --data-urlencode "codigo_moneda=1" \
  --data-urlencode "usuario_web=aqpa"
Respuesta:

json
{
  "deudas": [
    {
      "DESCRIPCION": "...",
      "IMPO_MAXI": 100.0,
      "IMPO_TOTA": 50.0,
      "MONE_CODI": 1,
      "FECH_VENC": "2025-08-01",
      "OBSERVACION": "...",
      "CODMOVIMIENTO": "...",
      "SEQ_DI": 123
    }
  ],
  "desc_clie": "Cliente Nombre",
  "cant_deta": 2,
  "codresp": "OK",
  "descresp": "Proceso exitoso",
  "idsession": 9876
}
🤝 Contribuciones
¡Se aceptan issues y pull requests! Para cambios importantes, por favor abre primero un issue describiendo tu propuesta.

📄 Licencia
Este proyecto no incluye archivo de licencia. Si deseas agregarla, crea un LICENSE en la raíz (ej. bajo MIT).
