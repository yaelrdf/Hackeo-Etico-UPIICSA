import requests
import json

url = 'http://localhost:5000/api/cita/1'
data = {
    'estado': 'cancelada',
    'apiClave': '1234567890'
}
response = requests.put(url, json=data)
print(response.json())