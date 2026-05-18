from fastapi import HTTPException, status

def not_found_exception(resource: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} no encontrado"
    )

def forbidden_exception():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permiso para realizar esta acción"
    )

def bad_request_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )