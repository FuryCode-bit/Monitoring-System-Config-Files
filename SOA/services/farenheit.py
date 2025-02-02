from flask import Flask, jsonify
import requests

app = Flask(__name__)

temperature = 77  # Temperatura inicial simulada

@app.route('/', methods=['GET'])
def get_temperature_fahrenheit():
    return jsonify({'temperature': temperature, 'unit': 'Fahrenheit'})

if __name__ == '__main__':
    # Registrar serviço no Registry automaticamente
    registry_url = 'http://0.0.0.0:5001/services'
    service_info = {
        'service_id': 1,
        'name': 'Fahrenheit Temperature Service',
        'endpoint': 'http://0.0.0.0:5003/'
    }
    
    # Retry mechanism for registering service
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(registry_url, json=service_info)
            if response.status_code == 201:
                print("Service registered successfully with ID:", response.json()["service_id"])
                break
            else:
                print("Failed to register service:", response.text)
                time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            time.sleep(2)
    
    app.run(host='0.0.0.0', port=5003)
