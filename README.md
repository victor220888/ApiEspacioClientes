# API Espacio Clientes

**Versión:** 1.0.0

## 📖 Descripción General

Este proyecto es una API RESTful construida con **FastAPI** y diseñada para gestionar el "Espacio Clientes" de la plataforma. La API se conecta a una base de datos **Oracle** para manejar las operaciones principales, como la consulta de deudas, la gestión de un carrito de pagos y el procesamiento de transacciones.

## 📋 Tabla de Contenidos

- [✨ Características Principales](#-características-principales)
- [⚡ Endpoints Principales](#-endpoints-principales)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [🚀 Guía de Inicio Rápido](#-guía-de-inicio-rápido)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación y Configuración](#instalación-y-configuración)
  - [Ejecutar la API](#ejecutar-la-api)
- [📖 Documentación Interactiva](#-documentación-interactiva)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🤝 Contribuciones](#-contribuciones)
- [📄 Licencia](#-licencia)

---

## ✨ Características Principales

*   **Autenticación Segura:** Implementa autenticación basada en **JSON Web Tokens (JWT)** para proteger los endpoints que requieren acceso de usuario.
*   **Gestión Completa de Pagos:**
    *   **Consulta de Deudas:** Permite a los usuarios verificar sus deudas pendientes.
    *   **Carrito de Compras:** Funcionalidad para agrupar múltiples deudas en una sola transacción de pago.
    *   **Procesamiento de Pagos:** Ejecuta la lógica para saldar las deudas seleccionadas.
    *   **Anulación de Transacciones:** Ofrece la capacidad de revertir un pago realizado.
*   **Backend Robusto y Moderno:**
    *   Construido sobre **FastAPI** para un alto rendimiento y **documentación interactiva automática** (vía Swagger UI y ReDoc).
    *   Validación estricta de datos de entrada y salida utilizando **Pydantic**.
    *   Conexión eficiente a **Oracle** a través de un pool de conexiones gestionado, asegurando escalabilidad y velocidad.
*   **Configuración Flexible:**
    *   Soporte para múltiples entornos (desarrollo/producción) a través de variables de entorno.
    *   **CORS (Cross-Origin Resource Sharing)** configurado para permitir peticiones solo desde los orígenes definidos en el archivo `.env`.

---

## ⚡ Endpoints Principales

#### `POST /token`
> Autentica un usuario y devuelve un token de acceso JWT.

*   **Request Body** (`application/x-www-form-urlencoded`):
    *   `username` (string)
    *   `password` (string)
*   **Response** (`200 OK`):
    ```json
    {
      "access_token": "<jwt_token>",
      "token_type": "bearer"
    }
    ```

#### `GET /consulta/deuda-cliente/`
> Obtiene todas las deudas pendientes de un cliente. Requiere autenticación.

*   **Headers:**
    *   `Authorization`: `Bearer <access_token>`
*   **Query Params:**
    *   `documento` (string, 6–15 chars)
    *   `moneda` (integer, ≥1)
*   **Response** (`200 OK`):
    ```json
    {
      "deudas": [
        {
          "DESCRIPCION": "Cuota de Préstamo",
          "IMPO_MAXI": 100.0,
          "IMPO_TOTA": 75.5,
          "MONE_CODI": 1,
          "FECH_VENC": "2025-08-01",
          "OBSERVACION": "Pago mensual",
          "CODMOVIMIENTO": "123",
          "SEQ_DI": 1
        }
      ],
      "desc_clie": "Nombre Apellido del Cliente",
      "cant_deta": 1,
      "codresp": "0",
      "descresp": "OK",
      "idsession": 42
    }
    ```

#### `POST /carrito/agregar`
> Agrega un movimiento (una deuda) al carrito de pagos del usuario. Requiere autenticación.

*   **Headers:**
    *   `Authorization`: `Bearer <access_token>`
*   **Query Params:**
    *   `idsession` (string, 1–9 chars)
    *   `indicador` (string, 1 char)
    *   `codmovimiento` (string, hasta 20 chars)
    *   `usuario` (string, hasta 35 chars)
*   **Response** (`200 OK`):
    ```json
    {
      "comision": 2.5,
      "codresp": "0",
      "descreps": "Agregado correctamente al carrito"
    }
    ```

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **FastAPI**
- **Uvicorn** (Servidor ASGI)
- **oracledb** (o `cx_Oracle`)
- **Pydantic** (Validación de datos y configuración)
- **PyJWT** (Para la seguridad con OAuth2 + JWT)
- **pytest** (Para pruebas de conexión)

---

## 🚀 Guía de Inicio Rápido

### Requisitos Previos
1.  **Python 3.10+** instalado.
2.  **Oracle Instant Client** o las librerías de cliente de Oracle necesarias para la conexión.
3.  `git` y `pip` disponibles en la línea de comandos de tu sistema.

### Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/victor220888/ApiEspacioClientes.git
    cd ApiEspacioClientes
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    *   *Windows (PowerShell):*
        ```bash
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        ```
    *   *Unix / macOS:*
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Instalar las dependencias:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto (puedes copiar `env.example` si existe) y completa los valores:
    ```dotenv
    # --- Configuración de la Base de Datos ---
    DB_USER=tu_usuario_oracle
    DB_PASSWORD=tu_contraseña
    DB_HOST=ip_o_host_del_servidor
    DB_SERVICE=nombre_del_servicio_oracle

    # --- Configuración del Pool de Conexiones ---
    ORACLE_POOL_MIN=2
    ORACLE_POOL_MAX=10
    ORACLE_POOL_INC=1

    # --- Configuración de JWT ---
    SECRET_KEY=un_secreto_muy_largo_y_dificil_de_adivinar
    TOKEN_ISSUER="api.mi-tierra.com"
    TOKEN_AUDIENCE="clientes"
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # --- Configuración de la Aplicación ---
    # Lista de orígenes permitidos en formato JSON
    ALLOWED_ORIGINS='["http://localhost:8000", "http://127.0.0.1:5500", "https://tu-frontend.com"]'
    ENVIRONMENT=development
    ```

5.  **Verificar la conexión a la base de datos:**
    Ejecuta el script de prueba para asegurarte de que tus credenciales y configuración son correctas.
    ```bash
    python test_db.py
    ```
    ✅ Si ves “Conexión exitosa!”, todo está listo.  
    ❌ Si hay un error, revisa las credenciales en tu archivo `.env` y la disponibilidad del servidor Oracle.

### Ejecutar la API

Para iniciar el servidor en modo de desarrollo (con recarga automática):
```bash
uvicorn api.api:app --reload --host 0.0.0.0 --port 8000
```

Alternativamente, puedes usar los scripts proporcionados, como:

```bash
.\start_https.bat
```

📖 Documentación Interactiva

Una vez que la API esté en funcionamiento, puedes acceder a la documentación generada automáticamente para probar los endpoints de forma interactiva:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

📁 Estructura del Proyecto

```Generated plaintext
ApiPagosWEB/
├── api/
│   ├── api.py             # Punto de entrada de la app y definición de routers
│   ├── auth.py            # Lógica de seguridad JWT y utilidades
│   ├── routes/            # Módulos con los endpoints agrupados por funcionalidad
│   └── models/            # Esquemas Pydantic para validación de datos
├── config/
│   ├── conexion.py        # Gestión del pool de conexiones a Oracle
│   └── settings.py        # Carga y validación de variables de entorno
├── requirements.txt       # Lista de dependencias del proyecto
├── test_db.py             # Script para probar la conexión a la base de datos
├── .env.example           # Plantilla para las variables de entorno
└── .gitignore             # Archivos y carpetas a ignorar por Git
```

🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, por favor abre primero un issue para discutir lo que te gustaría cambiar o agregar.

📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
