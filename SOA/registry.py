from flask import Flask, jsonify, request, abort
from uuid import uuid4

app = Flask(__name__)

# Registro de serviços, estrutura simples (armazenamento em memória)
services_registry = {}

# Listar todos os serviços registrados
@app.route('/', methods=['GET'])
def status():
    return "It is Working!"

# Listar todos os serviços registrados
@app.route('/services', methods=['GET'])
def list_services():
    return jsonify(services_registry)

# Obter detalhes de um serviço específico por ID
@app.route('/services/<service_id>', methods=['GET'])
def get_service(service_id):
    service = services_registry.get(service_id)
    if not service:
        abort(404, description="Service not found")
    return jsonify(service)

# Registrar um novo serviço
@app.route('/services', methods=['POST'])
def register_service():
    service_data = request.get_json()
    if not service_data or 'name' not in service_data or 'endpoint' not in service_data:
        abort(400, description="Invalid data")
    
    service_id = str(uuid4())  # Gera um ID único para o serviço
    services_registry[service_id] = service_data
    return jsonify({"service_id": service_id}), 201

# Atualizar um serviço existente (usando PUT)
@app.route('/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    if service_id not in services_registry:
        abort(404, description="Service not found")
    
    service_data = request.get_json()
    if not service_data or 'name' not in service_data or 'endpoint' not in service_data:
        abort(400, description="Invalid data")
    
    services_registry[service_id] = service_data
    return jsonify({"message": "Service updated"}), 200

# Remover um serviço do registry
@app.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    if service_id in services_registry:
        del services_registry[service_id]
        return jsonify({"message": "Service deleted"}), 200
    abort(404, description="Service not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
