"""
Flask Sessions Demo
A minimal demo showing session management in Flask
"""

from flask import Flask, session, request, jsonify, render_template_string
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'demo_secret_key_123'  # In production, use environment variable
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Simple user database
USERS = {
    'user1': {'password': 'pass123', 'nombre': 'Juan García'},
    'user2': {'password': 'pass456', 'nombre': 'María López'}
}


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flask Sessions Demo</title>
    <style>
        * { font-family: Arial, sans-serif; }
        body { 
            max-width: 600px; 
            margin: 40px auto; 
            padding: 20px; 
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .session-info {
            background: #e7f3ff;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 15px 0;
            border-radius: 4px;
        }
        .form-group {
            margin: 15px 0;
        }
        label { 
            display: block; 
            font-weight: bold; 
            margin-bottom: 5px;
            color: #333;
        }
        input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            padding: 10px 20px;
            margin: 5px 5px 5px 0;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        .btn-login { background: #28a745; color: white; }
        .btn-logout { background: #dc3545; color: white; }
        .btn-login:hover { background: #218838; }
        .btn-logout:hover { background: #c82333; }
        .status {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
        }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .session-id {
            font-family: monospace;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            word-break: break-all;
            font-size: 12px;
        }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Flask Sessions Demo</h1>
        
        <div id="loginForm">
            <div class="form-group">
                <label for="username">Usuario:</label>
                <input type="text" id="username" placeholder="user1 o user2">
            </div>
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" placeholder="pass123 o pass456">
            </div>
            <button class="btn-login" onclick="doLogin()">Iniciar Sesión</button>
            <div id="credentials" style="font-size: 12px; color: #666; margin-top: 15px;">
                <strong>Credenciales de prueba:</strong><br>
                user1 / pass123<br>
                user2 / pass456
            </div>
        </div>

        <div id="sessionDisplay" class="hidden">
            <div id="statusMessage" class="status"></div>
            
            <div class="session-info">
                <strong>👤 Usuario Autenticado:</strong><br>
                Nombre: <span id="displayName"></span><br>
                Usuario: <span id="displayUser"></span>
            </div>

            <div class="session-info">
                <strong>📍 Información de Sesión:</strong><br>
                <div style="margin-top: 10px;">
                    <strong>Session ID:</strong><br>
                    <div class="session-id" id="sessionId">-</div>
                </div>
                <div style="margin-top: 10px;">
                    <strong>Datos de Sesión:</strong><br>
                    <div class="session-id" id="sessionData">-</div>
                </div>
            </div>

            <button class="btn-logout" onclick="doLogout()">Cerrar Sesión</button>
        </div>

        <div id="notAuthMessage" class="session-info hidden">
            <strong>⚠️ Estado:</strong> No hay sesión activa
        </div>
    </div>

    <script>
        async function doLogin() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                alert('Por favor completa usuario y contraseña');
                return;
            }

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('loginForm').classList.add('hidden');
                    document.getElementById('notAuthMessage').classList.add('hidden');
                    document.getElementById('sessionDisplay').classList.remove('hidden');
                    document.getElementById('displayName').textContent = data.nombre;
                    document.getElementById('displayUser').textContent = data.username;
                    showStatus('✓ ' + data.message, 'success');
                    refreshSessionInfo();
                } else {
                    showStatus('✗ ' + data.message, 'error');
                }
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
            }
        }

        async function doLogout() {
            try {
                const response = await fetch('/api/logout', { method: 'POST' });
                const data = await response.json();
                
                document.getElementById('loginForm').classList.remove('hidden');
                document.getElementById('credentials').style.display = 'block';
                document.getElementById('sessionDisplay').classList.add('hidden');
                document.getElementById('notAuthMessage').classList.remove('hidden');
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
                showStatus('✓ ' + data.message, 'success');
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
            }
        }

        async function refreshSessionInfo() {
            try {
                const response = await fetch('/api/session-info');
                const data = await response.json();
                
                if (data.session_data) {
                    document.getElementById('sessionId').textContent = 
                        data.session_id || 'Cookie no disponible';
                    document.getElementById('sessionData').textContent = 
                        JSON.stringify(data.session_data, null, 2);
                }
            } catch (error) {
                console.error('Error refreshing session info:', error);
            }
        }

        function showStatus(message, type) {
            const elem = document.getElementById('statusMessage');
            elem.textContent = message;
            elem.className = 'status ' + type;
        }

        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                if (data.loggedin) {
                    document.getElementById('loginForm').classList.add('hidden');
                    document.getElementById('notAuthMessage').classList.add('hidden');
                    document.getElementById('sessionDisplay').classList.remove('hidden');
                    document.getElementById('displayName').textContent = data.nombre;
                    document.getElementById('displayUser').textContent = data.username;
                    refreshSessionInfo();
                } else {
                    document.getElementById('loginForm').classList.remove('hidden');
                    document.getElementById('sessionDisplay').classList.add('hidden');
                    document.getElementById('notAuthMessage').classList.remove('hidden');
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }

        // Check status on page load
        window.addEventListener('load', checkStatus);
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    """Home page - show HTML interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status', methods=['GET'])
def status():
    """Check authentication status"""
    if 'username' in session:
        return jsonify({
            'loggedin': True,
            'username': session.get('username'),
            'nombre': session.get('nombre')
        })
    return jsonify({'loggedin': False})


@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Validate credentials
    if username not in USERS or USERS[username]['password'] != password:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401
    
    # Create session
    session.permanent = True
    session['username'] = username
    session['nombre'] = USERS[username]['nombre']
    
    return jsonify({
        'success': True,
        'message': 'Login exitoso',
        'username': username,
        'nombre': USERS[username]['nombre']
    })


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint - destroy session"""
    username = session.get('username')
    session.clear()
    return jsonify({
        'success': True,
        'message': f'Sesión de {username} cerrada',
        'loggedin': False
    })


@app.route('/api/profile', methods=['GET'])
def profile():
    """Protected route - requires authentication"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'No autenticado'}), 401
    
    return jsonify({
        'username': session.get('username'),
        'nombre': session.get('nombre'),
        'message': f'Este es el perfil de {session.get("nombre")}'
    })


@app.route('/api/session-info', methods=['GET'])
def session_info():
    """Display current session information"""
    if 'username' not in session:
        return jsonify({'message': 'No hay sesión activa'})
    
    return jsonify({
        'session_data': dict(session),
        'session_id': request.cookies.get('session', 'No disponible')
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🔐 Flask Sessions Demo")
    print("=" * 50)
    print("\n✓ Servidor iniciado en: http://localhost:5000")
    print("\n📍 Abre tu navegador y visita:")
    print("   http://localhost:5000")
    print("\n💾 Puedes ver la Session ID en:")
    print("   DevTools → Application → Cookies")
    print("\n" + "=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
