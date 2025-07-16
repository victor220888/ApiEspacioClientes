from fastapi.concurrency import run_in_threadpool
from fastapi.security import OAuth2PasswordRequestForm

#rom streamlit import status # type: ignore
from fastapi import FastAPI, HTTPException, Depends, Query, status  # type: ignore

import cx_Oracle  # type: ignore
from cx_Oracle import DatabaseError # type: ignore
from config.settings import settings
from config import get_connection

from api.models import ConsultaDeudaResponse #Explicacion en el __init__.py del models
from api.models.carrito import AgregarCarritoResponse
from api.models.pago   import PagoResponse

from api.auth import create_access_token, get_current_user


import logging
from starlette.middleware.cors import CORSMiddleware # type: ignore
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # type: ignore
from starlette.middleware.trustedhost import TrustedHostMiddleware # type: ignore

# silencia los mensajes de versionado de bcrypt
logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

logger = logging.getLogger("uvicorn.error")
app = FastAPI(
    title="API Pagos Web (Espacio Clientes)",
    version="1.0.0",
    openapi_tags=[
                  {"name": "Login", "description": "Autenticación vía JWT"},
                  {"name": "Consulta", "description": "Obtener deudas del cliente"},
                  {"name": "Carrito", "description": "Agrega los servicios seleccionados desde la Web al carrito"},
                ]
)


# Habilita CORS para orígenes permitidos (local en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

'''
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

# Forzar HTTPS y Trusted Hosts solo en producción
if settings.environment == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["frontend.tu-dominio.com", "api.tu-dominio.com"]
    )


def db_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.post("/token",
    summary="Autenticar usuario y obtener token de acceso",
    tags=["Login"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn = Depends(db_conn)
):
    cur = conn.cursor()
    try:
        p_codresp  = cur.var(int)
        p_descresp = cur.var(str)
        cur.callproc(
            "PACK_PAGO_WS.VALIDAR_USURAIO",
            [
                form_data.username,
                p_codresp,
                p_descresp
            ]
        )
        codigo  = p_codresp.getvalue()
        mensaje = p_descresp.getvalue()
    finally:
        cur.close()

    if codigo != 0:
        raise HTTPException(status_code=codigo, detail=mensaje)

    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/consulta/deuda-cliente/",
    response_model=ConsultaDeudaResponse,
    summary="Retorna todas las deudas del cliente (incluye todos los servicios ya sea cuotas, jardinera, agua, impuesto, expensas, otros gastos) tanto para planes finalizados o activos",
    tags=["Consulta"],
    dependencies=[Depends(get_current_user)]
)
async def consultar_deuda(
    documento: str = Query(..., min_length=6, max_length=15),
    moneda: int    = Query(..., ge=1),
    usuario: str   = Query(..., min_length=3),
    conn = Depends(db_conn)
):
    try:
        cur: Cursor = conn.cursor()  # type: ignore
        p_deud      = cur.var(cx_Oracle.CURSOR)
        p_desc_clie = cur.var(str)
        p_cant_deta = cur.var(int)
        p_idsession = cur.var(int)
        p_codresp   = cur.var(str)
        p_descresp  = cur.var(str)

        cur.callproc(
            "pack_pago_ws.paweb_consulta",
            [
                documento,
                moneda,
                p_deud,
                usuario,
                p_desc_clie,
                p_cant_deta,
                p_idsession,
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
            "descresp":  p_descresp.getvalue()  or "",
            "idsession": p_idsession.getvalue() or 0
        }

    except DatabaseError as err:  # type: ignore
        logger.exception("Error BD al consultar deuda")
        raise HTTPException(500, detail="Error de base de datos.")
    except Exception as err:
        logger.exception("Error inesperado en consulta deuda")
        raise HTTPException(500, detail="Error interno.")
    finally:
        cur.close()


@app.post(
    "/carrito/agregar",
    response_model=AgregarCarritoResponse,
    summary="Agrega un movimiento al carrito",
    tags=["Carrito"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
async def agregar_al_carrito(
    idsession: str     = Query(..., description="ID de sesión único para la transacción.", min_length=1, max_length=9),
    indicador: str     = Query(..., description="El indicador determina si se agrega o quita un item del carrito. (S/N)", min_length=1, max_length=1),
    codmovimiento: str = Query(..., description="Código de la transacción a procesar.", min_length=1, max_length=20),
    usuario: str       = Query(..., description="Nombre de usuario que realiza la operación.", max_length=35),
    conn = Depends(db_conn)
):
    """
    Pudes usar este endpoint para sumar o restar un item al carrito.
    Los parametros `idsession`, y `codmovimiento` deben ser los datos que retornaron en la consulta de deuda.
    El `indicador` puede ser `S` para agregar o `N` para eliminar un item del carrito.
    """
    cur = conn.cursor()
    try:
        # Variables de salida
        p_comision = cur.var(float)
        p_codresp  = cur.var(str)
        p_descreps = cur.var(str)

        # Llamada al paquete Oracle
        cur.callproc(
            "PACK_PAGO_WS.AGREGAR_AL_CARRITO",
            [
                idsession,
                indicador,
                codmovimiento,
                usuario,
                p_comision,
                p_codresp,
                p_descreps
            ]
        )
        # Si la operación modifica datos, confirma la transacción
        conn.commit()

        # Construye la respuesta
        return AgregarCarritoResponse(
            comision   = p_comision.getvalue(),
            codresp    = p_codresp.getvalue(),
            descreps   = p_descreps.getvalue()
        )
    except cx_Oracle.DatabaseError as err:
        logger.exception("Error BD al agregar al carrito")
        # Extrae código y mensaje si tu paquete los devuelve en excepciones
        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al agregar al carrito."
        )
    finally:
        cur.close()
        
        

@app.post(
    "/pago",
    response_model=PagoResponse,
    summary="Procesa el pago de un o los servicio de un cliente",
    tags=["Pago"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
async def confirmar_pago(
    session:         str = Query(..., description="En la respuesta de la consulta puedes obtener el ID de sesión único.", min_length=1, max_length=9),
    user:            str = Query(..., description="Usuario medio alternativo." , max_length=35),
    cod_transaccion: str = Query(..., description="Código de la transacción a procesar (emite la entidad bancaria)."   , max_length=20),
    conn = Depends(db_conn)
):
    """
    Este endpoint procesa un pago utilizando los datos proporcionados.
    Llama al procedimiento almacenado 'pack_pago_ws.paweb_pago'.
    
    - **session**: ID de la sesión de la consulta.
    - **user**: Usuario que realiza la operación.
    - **cod_transaccion**: Código de la transacción a ejecutar.
    """
    # 1. Validamos los datos de entrada.
    if not session or not user or not cod_transaccion:
        raise HTTPException(status_code=400, detail="Faltan datos requeridos.")

    # 2. Definimos una función síncrona anidada para la lógica de BD.
    #    Esto nos permite pasarla a run_in_threadpool y no bloquear FastAPI.
    def db_call(connection):
        try:
            cursor = conn.cursor()

            # Declarar variables para los parámetros de SALIDA
            o_codresp = cursor.var(str)
            o_mod_fact = cursor.var(int)
            o_descresp = cursor.var(str)

            # Llamar al procedimiento almacenado
            cursor.callproc(
                "pack_pago_ws.paweb_pago",
                [
                    session,         # i_session
                    user,            # i_user
                    cod_transaccion, # i_codtransaccion
                    o_codresp,       # o_codresp
                    o_mod_fact,      # o_mod_fact
                    o_descresp       # o_descresp
                ]
            )
            
            # Obtener los valores de salida
            result = {
                "cod_resp": o_codresp.getvalue(),
                "mod_fact": o_mod_fact.getvalue(),
                "desc_resp": o_descresp.getvalue()
            }
            cursor.close()
            return result

        except cx_Oracle.DatabaseError as err:
            print(f"Error en la base de datos al procesar el pago: {err}")
            return None

    # 3. Ejecutamos la función de BD en un hilo separado
    result_dict = await run_in_threadpool(db_call, db_conn)

    # 4. Manejamos los resultados
    if result_dict is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error en el servidor al procesar el pago."
        )

    # Si el código de respuesta del procedimiento indica un error de negocio
    if result_dict.get("cod_resp") != "0":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en el pago: {result_dict.get('desc_resp')}"
        )
    
    # Si todo salió bien, devolvemos el resultado.
    # FastAPI lo validará contra el modelo PagoResponse.
    return result_dict