"""
Basic Authentication Demo
A standalone demo program showing simple authentication with role-based access
"""

# Simple user database
USERS = {
    'paciente1': {'password': 'pass123', 'rol': 'paciente', 'nombre': 'Juan García'},
    'doctor1': {'password': 'doc456', 'rol': 'doctor', 'nombre': 'Dr. López'},
    'admin1': {'password': 'admin789', 'rol': 'admin', 'nombre': 'Admin User'}
}

# Global session storage
session = None

def login(username, password):
    """Authenticate user and create session"""
    global session
    
    if username not in USERS:
        return False, "Usuario no encontrado"
    
    user = USERS[username]
    if user['password'] != password:
        return False, "Contraseña incorrecta"
    
    session = {
        'username': username,
        'nombre': user['nombre'],
        'rol': user['rol'],
        'loggedin': True
    }
    return True, "Login exitoso"

def logout():
    """Clear session"""
    global session
    session = None
    return "Sesión cerrada"

def dashboard():
    """Display dashboard based on user role"""
    global session
    
    if session is None:
        return "Error: No está autenticado. Use login(username, password)"
    
    rol = session.get('rol')
    nombre = session.get('nombre')
    
    if rol == 'paciente':
        return f"Bienvenido {nombre} (Paciente)\n- Ver citas\n- Ver resultados médicos"
    elif rol == 'doctor':
        return f"Bienvenido Dr. {nombre} (Doctor)\n- Ver pacientes\n- Crear prescripciones"
    elif rol == 'admin':
        return f"Bienvenido {nombre} (Admin)\n- Gestionar usuarios\n- Ver reportes"
    
    return "Rol desconocido"

def check_auth(required_rol=None):
    """Check if user is authenticated and has required role"""
    global session
    
    if session is None:
        return False
    
    if required_rol and session.get('rol') != required_rol:
        return False
    
    return True

# Demo execution
if __name__ == '__main__':
    print("=== Demo de Autenticación ===\n")
    
    # Test 1: Successful login
    print("Test 1: Login como paciente")
    success, msg = login('paciente1', 'pass123')
    print(f"Resultado: {msg}")
    if success:
        print(f"Dashboard:\n{dashboard()}\n")
    
    # Test 2: Wrong password
    print("Test 2: Login con contraseña incorrecta")
    success, msg = login('doctor1', 'wrongpass')
    print(f"Resultado: {msg}\n")
    
    # Test 3: Non-existent user
    print("Test 3: Usuario que no existe")
    success, msg = login('unknown', 'pass123')
    print(f"Resultado: {msg}\n")
    
    # Test 4: Doctor login
    print("Test 4: Login como doctor")
    success, msg = login('doctor1', 'doc456')
    print(f"Resultado: {msg}")
    if success:
        print(f"Dashboard:\n{dashboard()}\n")
    
    # Test 5: Admin login
    print("Test 5: Login como admin")
    success, msg = login('admin1', 'admin789')
    print(f"Resultado: {msg}")
    if success:
        print(f"Dashboard:\n{dashboard()}\n")
    
    # Test 6: Logout
    print("Test 6: Logout")
    print(logout())
    print(f"Dashboard después de logout: {dashboard()}")