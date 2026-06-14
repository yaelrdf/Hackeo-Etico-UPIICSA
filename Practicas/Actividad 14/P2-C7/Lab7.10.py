# auth.py
import bcrypt

def hash_password(password):
    # Genera una sal y hashea la contraseña
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password, hashed_password):
    # Verifica si la contraseña en texto plano coincide con el hash
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

if __name__ == '__main__':
    # Ejemplo de uso
    password = "MiContraseñaSegura123!"
    hashed = hash_password(password)
    print(f"Hash generado: {hashed}")
    is_valid = check_password("MiContraseñaSegura124!", hashed)
    print(f"¿La contraseña es válida? {is_valid}")