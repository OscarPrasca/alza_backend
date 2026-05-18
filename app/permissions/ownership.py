from app.utils.exceptions import forbidden_exception

def check_ownership(resource_user_id: str, current_user_id: str):
    if str(resource_user_id) != str(current_user_id):
        forbidden_exception()
        