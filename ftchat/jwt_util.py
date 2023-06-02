import jwt

def get_value_from_jwt(jwt_token, key):
    try:
        decoded_token = jwt.decode(jwt_token, verify=False)
        return decoded_token.get(key)
    except jwt.InvalidTokenError:
        return None
    
def get_uid_from_jwt(jwt_token):
    return get_value_from_jwt(jwt_token, 'user_id')