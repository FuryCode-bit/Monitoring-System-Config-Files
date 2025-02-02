import pika
import time
import random

def publish_temperature():
    # Conexão com RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Criar uma exchange do tipo 'topic'
    channel.exchange_declare(exchange='temperature_exchange', exchange_type='topic')

    while True:
        temperature_celsius = random.uniform(20, 30)
        temperature_fahrenheit = temperature_celsius * 9/5 + 32

        # Publicar temperatura em Celsius
        channel.basic_publish(
            exchange='temperature_exchange',
            routing_key='temperature.celsius',
            body=str(temperature_celsius)
        )
        print(f"Published Celsius temperature: {temperature_celsius}")

        # Publicar temperatura em Fahrenheit
        channel.basic_publish(
            exchange='temperature_exchange',
            routing_key='temperature.fahrenheit',
            body=str(temperature_fahrenheit)
        )
        print(f"Published Fahrenheit temperature: {temperature_fahrenheit}")

        # Esperar 30 segundos
        time.sleep(30)

    connection.close()

if __name__ == '__main__':
    publish_temperature()
