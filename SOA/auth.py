# Autenticação e Controle de Acesso
from flask import Flask, request, jsonify, abort
import hashlib

app = Flask(__name__)
users = {}
services = {"Celsius": 5002, "Fahrenheit": 5003}

# Registro de usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, "Invalid data")

    username = data['username']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    if username in users:
        abort(400, "User already exists")

    users[username] = {"password": password, "unit": data.get('unit', 'Celsius')}
    return jsonify({"message": "User registered"}), 201

# Autenticação e obtenção de serviço
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, "Invalid data")

    username = data['username']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    user = users.get(username)
    if not user or user['password'] != password:
        abort(401, "Invalid credentials")

    unit = user['unit']
    service_port = services.get(unit)
    if not service_port:
        abort(404, "Service not found")

    return jsonify({"service": f"http://localhost:{service_port}/"}), 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)