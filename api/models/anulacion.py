# api/models/anulacion.py
from pydantic import BaseModel

class AnulacionResponse(BaseModel):
    cod_resp: str
    desc_resp: str