# API Pagos Web (Espacio Clientes)

**Versión:** 1.0.0

---

## 📖 Descripción

Este proyecto es una API REST construida con **FastAPI** para el “Espacio Clientes” de Pagos Web. Permite:

- Autenticación vía JWT.
- Consulta de deudas de clientes contra una base de datos Oracle.
- Manejo de pool de conexiones con **cx_Oracle**.
- Validación de datos de entrada con **Pydantic**.
- Configuración de CORS y entornos (desarrollo / producción).

---

## ✨ Características

- **/token** (POST): Obtiene un token JWT a partir de credenciales.
- **/epacio-cliente/consultar-deuda/** (GET): Consulta deudas de un cliente (requiere token).
- Pool de conexiones Oracle configurable.
- Soporte para CORS según orígenes definidos en variables de entorno.
- Documentación automática Swagger y ReDoc.

---

## 🛠 Requisitos

- Python 3.10 o superior  
- Oracle Instant Client instalado (para `cx_Oracle`)  
- Git  

---

## 🚀 Instalación

1. Clona este repositorio y accede a la carpeta:
   ```bash
   git clone https://github.com/tu-usuario/ApiPagosWEB.git
   cd ApiPagosWEB
Crea y activa un entorno virtual:

bash
Copiar
Editar
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate
# macOS/Linux:
source .venv/bin/activate
Instala las dependencias:

bash
Copiar
Editar
pip install --upgrade pip
pip install -r requirements.txt
⚙️ Configuración
Abre y edita el archivo .env en la raíz del proyecto. Ajusta los valores según tu entorno:

dotenv
Copiar
Editar
DB_USER=adcs
DB_PASSWORD=centu
DB_HOST=192.168.13.64
DB_SERVICE=OMEGA
ORACLE_POOL_MIN=2
ORACLE_POOL_MAX=10
ORACLE_POOL_INC=1

SECRET_KEY=tu_clave_ultra_larga_y_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ALLOWED_ORIGINS='["http://localhost:8000","http://127.0.0.1:8000"]'
ENVIRONMENT=development
(Opcional) Revisa y ajusta los parámetros de pool en config/settings.py si lo necesitas.

📁 Estructura del proyecto
bash
Copiar
Editar
ApiPagosWEB/
├── api/
│   ├── api.py                 # Definición de endpoints y lógica principal
│   ├── auth.py                # Seguridad JWT y utilidades
│   └── models/deuda.py        # Esquemas Pydantic para respuesta de deuda
├── config/
│   ├── conexion.py            # Pool de conexiones Oracle
│   └── settings.py            # Carga de variables de entorno
├── requirements.txt           # Lista de dependencias
├── .env                       # Variables de entorno (edítalo)
├── .gitignore
└── prueba.html                # Cliente web de ejemplo para login y consulta
🏃‍♂️ Uso
Inicia la API en modo desarrollo:

bash
Copiar
Editar
uvicorn api.api:app --reload
Abre en tu navegador:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Obtener token

bash
Copiar
Editar
curl -X POST "http://localhost:8000/token" \
  -d "username=aqpa&password=123456"
json
Copiar
Editar
{
  "access_token": "<tu_jwt_token>",
  "token_type": "bearer"
}
Consultar deuda
Reemplaza <tu_jwt_token> y ajusta los parámetros:

bash
Copiar
Editar
curl -G "http://localhost:8000/epacio-cliente/consultar-deuda/" \
  -H "Authorization: Bearer <tu_jwt_token>" \
  --data-urlencode "nro_documento_cliente=4510123" \
  --data-urlencode "codigo_moneda=1" \
  --data-urlencode "usuario_web=aqpa"
json
Copiar
Editar
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
    },
    …
  ],
  "desc_clie": "Cliente Nombre",
  "cant_deta": 2,
  "codresp": "OK",
  "descresp": "Proceso exitoso",
  "idsession": 9876
}
Cliente web de prueba
Abre prueba.html en tu navegador para probar login y consulta desde una interfaz sencilla.

🤝 Contribuciones
¡Se aceptan issues y pull requests! Para cambios importantes, por favor abre primero un issue describiendo tu propuesta.

📄 Licencia
Este proyecto no incluye archivo de licencia. Si deseas agregarla, crea un LICENSE en la raíz, por ejemplo bajo MIT.
