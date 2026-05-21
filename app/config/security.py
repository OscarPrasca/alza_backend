import json
import urllib.request
import logging
from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config.settings import settings

logger = logging.getLogger(__name__)

# Cache en memoria para JWKS de ES256 (evita peticiones HTTP en cada llamada)
_cached_jwks = None

def _get_jwks(jwks_url: str) -> dict:
    global _cached_jwks
    if _cached_jwks is None:
        try:
            logger.info(f"Obteniendo JWKS de Supabase desde: {jwks_url}")
            req = urllib.request.Request(
                jwks_url,
                headers={"User-Agent": "FastAPI-Supabase-Auth"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                _cached_jwks = json.loads(response.read().decode())
                logger.info("JWKS obtenido y guardado en cache con éxito.")
        except Exception as e:
            logger.error(f"Error al obtener JWKS desde Supabase: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo obtener la clave pública para verificar la firma del token."
            )
    return _cached_jwks

def verify_jwt_token(token: str) -> dict:
    try:
        # Obtener la cabecera sin verificar para determinar el algoritmo (HS256 o ES256)
        header = jwt.get_unverified_header(token)
        alg = header.get("alg", "HS256")
        logger.info(f"Token recibido con algoritmo: {alg}")

        if alg == "ES256":
            # Autenticación asimétrica de Supabase (Nueva por defecto)
            jwks_url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1/jwks"
            jwks = _get_jwks(jwks_url)
            
            kid = header.get("kid")
            if not kid:
                logger.error("Token ES256 no contiene 'kid' en su cabecera")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido: falta 'kid'"
                )
                
            public_key = None
            for key in jwks.get("keys", []):
                if key.get("kid") == kid:
                    public_key = key
                    break
                    
            if not public_key:
                # Si no se encuentra el kid, limpiamos caché por si Supabase rotó sus llaves públicas
                logger.warning("Clave no encontrada en cache, limpiando caché e intentando de nuevo...")
                global _cached_jwks
                _cached_jwks = None
                jwks = _get_jwks(jwks_url)
                for key in jwks.get("keys", []):
                    if key.get("kid") == kid:
                        public_key = key
                        break
                        
            if not public_key:
                logger.error(f"No se encontró clave pública en JWKS para kid: {kid}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Firma del token no pudo ser verificada: clave no encontrada"
                )
                
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["ES256"],
                options={"verify_aud": False}
            )
        else:
            # Autenticación clásica simétrica (HS256)
            logger.info("Usando validación clásica HS256")
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error("Token decodificado pero el claim 'sub' (User ID) es nulo")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: sujeto no identificado"
            )
            
        logger.info(f"Token verificado con éxito para user_id: {user_id}")
        return payload

    except JWTError as e:
        logger.error(f"Error de JWTError al decodificar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}"
        )