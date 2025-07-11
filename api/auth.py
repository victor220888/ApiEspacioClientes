# api/auth.py
import uuid
from datetime import datetime, timedelta

from jose import JWTError, jwt # type: ignore
from passlib.context import CryptContext # type: ignore
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from config.settings import settings

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para extraer el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña en texto plano coincida con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashea la contraseña para almacenamiento seguro.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    jti = str(uuid.uuid4())

    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": settings.token_issuer,
        "aud": settings.token_audience,
        "jti": jti,
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exc = HTTPException(
        status_code=401,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            audience=settings.token_audience,
            issuer=settings.token_issuer
        )
        user: str = payload.get("sub")
        if not user:
            raise credentials_exc

        # Aquí podrías comprobar revocación de tokens por jti si lo implementas
        # jti = payload.get("jti")
        # if is_token_revoked(jti):
        #     raise credentials_exc

    except JWTError:
        raise credentials_exc

    return user
