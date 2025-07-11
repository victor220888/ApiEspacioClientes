import cx_Oracle # type: ignore
from cx_Oracle import DatabaseError 
import logging
from .settings import settings

logger = logging.getLogger(__name__)

dsn = cx_Oracle.makedsn(
    settings.db_host,
    1521,
    service_name=settings.db_service
)

pool = cx_Oracle.SessionPool(
    user=settings.db_user,
    password=settings.db_password,
    dsn=dsn,
    min=settings.oracle_min,
    max=settings.oracle_max,
    increment=settings.oracle_increment,
    encoding="UTF-8"
)

def get_connection():
    try:
        return pool.acquire()
    #except cx_Oracle.Error as e:
    #    logger.error("No se pudo adquirir conexión Oracle: %s", e)
    #    raise
    except DatabaseError as err:  # Ahora DatabaseError está definido
        logger.exception("Error BD al consultar deuda")
        raise HTTPException(500, detail="Error de base de datos.")