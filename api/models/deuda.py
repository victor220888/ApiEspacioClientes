# api/models/deuda.py

from typing import Optional
from pydantic import BaseModel # type: ignore
from pydantic import ConfigDict # type: ignore

class DeudaItem(BaseModel):
    DESCRIPCION: str
    IMPO_MAXI: float
    IMPO_TOTA: float
    MONE_CODI: int
    FECH_VENC: str
    OBSERVACION: str
    CODMOVIMIENTO: str
    SEQ_DI: int

    # Ignora cualquier otro campo extra que venga en el JSON
    model_config = ConfigDict(extra="ignore")


class ConsultaDeudaResponse(BaseModel):
    deudas: list[DeudaItem]
    desc_clie: Optional[str]    = None
    cant_deta: Optional[int]    = None
    codresp:  Optional[str]     = None
    descresp: Optional[str]     = None

    model_config = ConfigDict(extra="ignore")
