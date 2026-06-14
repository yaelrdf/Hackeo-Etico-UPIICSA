from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/api/cita/<int:id>', methods=['GET'])
def get_cita(id):
    # Simulación de base de datos
    cita = {
        'id': id,
        'paciente': 'Juan Pérez',
        'dentista': 'Dra. Ana',
        'fecha': '2026-06-15 10:00',
        'estado': 'confirmada'
    }
    return jsonify({
        'mensaje': 'Cita recuperada exitosamente',
        'codigo_http': 200,
        'cita': cita
    })

if __name__ == '__main__':
    app.run(debug=True)