from flask import Flask, redirect, url_for, session, request, render_template_string
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)

# ============ PUT YOUR SECRET KEY HERE ============
# Generate a random secret key for session management
app.secret_key = 'client1-secret-key'
# ================================================

oauth = OAuth(app)

# ============ PUT YOUR GOOGLE CREDENTIALS HERE ============
# Get these from: https://console.cloud.google.com/
# 1. Create a project
# 2. Enable Google+ API
# 3. Create OAuth 2.0 credentials (Web application)
# 4. Add http://localhost:5000/authorize to Authorized redirect URIs
google = oauth.register(
    name='google',
    client_id='',  # Replace this
    client_secret='',  # Replace this
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)
# =========================================================

# HTML templates
LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Google OAuth Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        .login-btn {
            background: #4285F4;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .login-btn:hover {
            background: #357ae8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Google OAuth Demo</h1>
        <p>Login to see your Google account information</p>
        <a href="/login"><button class="login-btn">Login with Google</button></a>
    </div>
</body>
</html>
'''

DASHBOARD_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4285F4;
            padding-bottom: 10px;
        }
        .info-box {
            background: #f5f5f5;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #4285F4;
            border-radius: 5px;
        }
        .info-label {
            font-weight: bold;
            color: #555;
            margin-bottom: 5px;
        }
        .info-value {
            color: #333;
            word-break: break-all;
            font-family: monospace;
        }
        .logout-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
            transition: background 0.3s;
        }
        .logout-btn:hover {
            background: #c82333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Welcome, {{ name }}!</h1>
        
        <div class="info-box">
            <div class="info-label">📧 Email:</div>
            <div class="info-value">{{ email }}</div>
        </div>

        <div class="info-box">
            <div class="info-label">🆔 Session ID:</div>
            <div class="info-value">{{ session_id }}</div>
        </div>

        <div class="info-box">
            <div class="info-label">👤 User ID:</div>
            <div class="info-value">{{ user_id }}</div>
        </div>

        <div class="info-box">
            <div class="info-label">📸 Profile Picture:</div>
            <div class="info-value">
                <img src="{{ picture }}" alt="Profile" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover;">
            </div>
        </div>

        <div class="info-box">
            <div class="info-label">📝 Full User Data:</div>
            <div class="info-value">{{ user_data }}</div>
        </div>

        <a href="/logout"><button class="logout-btn">Logout</button></a>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Home page - login page"""
    return render_template_string(LOGIN_PAGE)

@app.route('/login')
def login():
    """Redirect to Google OAuth login"""
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    """Handle OAuth callback from Google"""
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        userinfo = resp.json()
        
        # Store user data in session
        session['user'] = userinfo
        session['email'] = userinfo.get('email', 'N/A')
        
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f'Error during authorization: {str(e)}'

@app.route('/dashboard')
def dashboard():
    """Display user information after successful login"""
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user = session['user']
    session_id = request.cookies.get('session', 'N/A')
    
    return render_template_string(
        DASHBOARD_PAGE,
        name=user.get('name', 'User'),
        email=user.get('email', 'N/A'),
        user_id=user.get('id', 'N/A'),
        picture=user.get('picture', ''),
        session_id=session_id,
        user_data=str(user)
    )

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='localhost', port=5000)