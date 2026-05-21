from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def verify_jwt_token(token: str) -> dict:
    try:
        logger.info(f"Token recibido: {token[:50]}...")
        logger.info(f"JWT Secret configurado: {settings.SUPABASE_JWT_SECRET[:20]}...")
        
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        logger.info(f"Token válido para user_id: {user_id}")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return payload
    except JWTError as e:
        logger.error(f"JWTError: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}"
        )