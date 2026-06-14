from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Bazar de Ciudades</title></head>
<body>
    <h1>Bazar de Ciudades</h1>
    <p>Elija un servicio:</p>
    <a href="/ciudades">Paquetes de ciudades</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)