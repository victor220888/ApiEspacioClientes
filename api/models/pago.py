# api/models/pago.py
from pydantic import BaseModel, validator

# Modelo para los datos de ENTRADA que esperamos en el body del POST
class PagoInput(BaseModel):
    session: int
    user: str
    cod_transaccion: str

    @validator('user')
    def user_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El usuario no puede estar vacío')
        return v

    @validator('cod_transaccion')
    def cod_transaccion_formato(cls, v):
        if len(v) < 5:
            raise ValueError('El código de transacción debe tener al menos 5 caracteres')
        return v

# Modelo para los datos de SALIDA que devolverá nuestra API
class PagoResponse(BaseModel):
    cod_resp: str
    mod_fact: str
    desc_resp: str