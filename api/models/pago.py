# api/models/pago.py
from pydantic import BaseModel

# Modelo para los datos de ENTRADA que esperamos en el body del POST
class PagoInput(BaseModel):
    session: int
    user: str
    cod_transaccion: str

# Modelo para los datos de SALIDA que devolverá nuestra API
class PagoResponse(BaseModel):
    cod_resp: str
    mod_fact: str
    desc_resp: str