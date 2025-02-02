import requests

def get_service_info(unit):
    registry_url = 'http://0.0.0.0:5001/services'
    try:
        response = requests.get(registry_url)
        services = response.json()
        
        # Procura por um serviço que devolva a unidade de temperatura correta
        for service_id, service_info in services.items():
            if unit.lower() in service_info['name'].lower():
                return service_info['endpoint']
        
        print(f"No service found for {unit}")
        return None
    except Exception as e:
        print("Error querying the registry:", str(e))
        return None

def get_temperature(unit):
    endpoint = get_service_info(unit)
    if endpoint:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                print(f"Temperature: {data['temperature']} {data['unit']}")
            else:
                print("Failed to get temperature:", response.text)
        except Exception as e:
            print("Error calling service:", str(e))

if __name__ == '__main__':
    unit = input("Enter the unit of temperature (Celsius/Fahrenheit): ")
    get_temperature(unit)
