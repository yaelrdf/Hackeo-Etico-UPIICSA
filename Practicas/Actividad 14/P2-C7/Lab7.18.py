from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'client1-secret-key'

@app.route('/api/cita/<int:id>', methods=['PUT'])
def put_cita(id):
    if not request.json:
        return jsonify({'mensaje': 'No se enviaron datos', 'codigo_http': 400})
    api_clave = request.json.get('apiClave')
    if api_clave != '1234567890':
        return jsonify({'mensaje': 'Clave API inválida', 'codigo_http': 401})
    # Actualizar en BD
    return jsonify({
        'mensaje': 'Servicio PUT ejecutado',
        'codigo_http': 200,
        'id': id,
        'nuevo_estado': request.json.get('estado')
    })
    
if __name__ == '__main__':
    app.run(debug=True)