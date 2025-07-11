# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cx_Oracle

from configuracion.conexion import conexion, const as const             # tus constantes de conexión

app = FastAPI()


class ConsultaRequest(BaseModel):
    nrodocumento: str
    mone_codi: int
    user_comi: str   # corresponde a P_USER o P_USER_COMI
    # si tu procedimiento necesita P_TIPO_SERV, agrégalo aquí:
    tipo_serv: int = 1


class ConsultaResponse(BaseModel):
    desc_clie: str
    cant_deta: int
    codresp: str
    descresp: str
    deudas: list[dict]


@app.post("/consulta", response_model=ConsultaResponse)
def consulta(req: ConsultaRequest):
    try:
        # 1) Abrir conexión y cursor
        cx = conexion.conectar(
            const.USER,
            const.LOGIN,
            const.HOST,
            const.SCHEMA,
            const.SERVER_NAME
        )
        cursor = cx.cursor()

        # 2) Preparar variables de salida
        deud_var      = cursor.var(cx_Oracle.CURSOR)
        desc_clie_var = cursor.var(cx_Oracle.STRING)
        cant_deta_var = cursor.var(cx_Oracle.NUMBER)
        codresp_var   = cursor.var(cx_Oracle.STRING)
        descresp_var  = cursor.var(cx_Oracle.STRING)

        # 3) Ejecutar bloque PL/SQL que invoca al procedimiento empaquetado
        cursor.execute("""
        BEGIN
          pack_pago_ws.paweb_consulta(
            p_nrodocumento => :p_nrodocumento,
            p_mone_codi    => :p_mone_codi,
            p_deud         => :p_deud,
            p_user         => :p_user,
            p_desc_clie    => :p_desc_clie,
            p_cant_deta    => :p_cant_deta,
            p_codresp      => :p_codresp,
            p_descresp     => :p_descresp
          );
        END;
        """, {
            "p_nrodocumento": req.nrodocumento,
            "p_mone_codi":    req.mone_codi,
            "p_deud":         deud_var,
            "p_user":         req.user_comi,
            "p_desc_clie":    desc_clie_var,
            "p_cant_deta":    cant_deta_var,
            "p_codresp":      codresp_var,
            "p_descresp":     descresp_var,
        })

        # 4) Leer REF CURSOR y construir lista de dicts
        ref_cursor = deud_var.getvalue()
        cols = [col[0].lower() for col in ref_cursor.description]
        deudas = [dict(zip(cols, row)) for row in ref_cursor]

        # 5) Enviar respuesta
        return ConsultaResponse(
            desc_clie = desc_clie_var.getvalue(),
            cant_deta = int(cant_deta_var.getvalue()),
            codresp   = codresp_var.getvalue(),
            descresp  = descresp_var.getvalue(),
            deudas    = deudas
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        cx.close()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
