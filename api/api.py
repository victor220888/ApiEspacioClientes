# APIPAGOSWEB/api/api.py

from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from api.auth import create_access_token, verify_password, get_current_user, get_password_hash

from fastapi import FastAPI, HTTPException, Depends, Query  # type: ignore

import cx_Oracle  # type: ignore
from config.settings import settings
from config import get_connection

from api.models import DeudaItem, ConsultaDeudaResponse

import logging

# silencia los mensajes de versionado de bcrypt
logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

logger = logging.getLogger("uvicorn.error")
app = FastAPI(
    title="API Pagos Web (Espacio Clientes)",
    version="1.0.0",
    openapi_tags=[{"name": "Consulta", "description": "Obtener deudas del cliente"}]
)

from starlette.middleware.cors import CORSMiddleware # type: ignore
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # type: ignore
from starlette.middleware.trustedhost import TrustedHostMiddleware # type: ignore

# Habilita CORS para orígenes permitidos (local en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Forzar HTTPS y Trusted Hosts solo en producción
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["frontend.tu-dominio.com", "api.tu-dominio.com"]
    )


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # aquí deberías validar contra tu base de datos; este es un ejemplo hardcodeado:
    fake_user = {"username": "aqpa", "hashed_password": get_password_hash("123456")}
    if form_data.username != fake_user["username"] or not verify_password(form_data.password, fake_user["hashed_password"]):
        raise HTTPException(400, "Usuario o contraseña incorrectos")
    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


def db_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get(
    "/epacio-cliente/consultar-deuda/",
    response_model=ConsultaDeudaResponse,
    summary="Consulta deudas de un cliente",
    tags=["Consulta"],
    dependencies=[Depends(get_current_user)]
)
async def consultar_deuda(
    nro_documento_cliente: str = Query(..., min_length=6, max_length=12),
    codigo_moneda: int        = Query(..., ge=1),
    usuario_web: str          = Query(..., min_length=3),
    conn = Depends(db_conn)
):
    try:
        cur: Cursor = conn.cursor()  # type: ignore
        p_deud      = cur.var(cx_Oracle.CURSOR)
        p_desc_clie = cur.var(str)
        p_cant_deta = cur.var(int)
        p_codresp   = cur.var(str)
        p_descresp  = cur.var(str)

        cur.callproc(
            "pack_pago_ws.paweb_consulta",
            [
                nro_documento_cliente,
                codigo_moneda,
                p_deud,
                usuario_web,
                p_desc_clie,
                p_cant_deta,
                p_codresp,
                p_descresp
            ]
        )

        deuda_cur = p_deud.getvalue()
        items = []
        if deuda_cur:
            cols = [c[0] for c in deuda_cur.description]
            for row in deuda_cur:
                items.append(dict(zip(cols, row)))
            deuda_cur.close()

        return {
            "deudas": items,
            "desc_clie": p_desc_clie.getvalue() or "",
            "cant_deta": p_cant_deta.getvalue() or 0,
            "codresp":   p_codresp.getvalue()   or "",
            "descresp":  p_descresp.getvalue()  or ""
        }

    except DatabaseError as err:  # type: ignore
        logger.exception("Error BD al consultar deuda")
        raise HTTPException(500, detail="Error de base de datos.")
    except Exception as err:
        logger.exception("Error inesperado en consulta deuda")
        raise HTTPException(500, detail="Error interno.")
    finally:
        cur.close()
