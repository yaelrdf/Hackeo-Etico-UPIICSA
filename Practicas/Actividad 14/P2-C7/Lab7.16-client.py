import requests
import json

url = 'http://localhost:5000/api/cita/1'
response = requests.get(url)
data = response.json()
print(f"Mensaje: {data['mensaje']}")
print(f"Código http: {data['codigo_http']}")
print(f"Cita: {data['cita']}")