# api/models/carrito.py

from pydantic import BaseModel
from typing import Optional

class AgregarCarritoRequest(BaseModel):
    idsession: int
    indicador: int
    codmovimiento: int
    user: str

class AgregarCarritoResponse(BaseModel):
    comision: Optional[float] = None
    codresp: str
    descreps: str
