import jwt
import time

class IdP:
    def __init__(self, credenciales):
        self.credenciales = credenciales
    
    def get_token(self):
        # Agregar expiración
        payload = self.credenciales.copy()
        payload['exp'] = time.time() + 3600
        token = jwt.encode(payload, 'secret_server_key', algorithm='HS256')
        return token
