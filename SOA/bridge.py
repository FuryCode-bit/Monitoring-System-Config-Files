# Bridge de Persistência
import pika
import sqlite3

def persist_temperature():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='temperature_exchange', exchange_type='topic')

    queue = channel.queue_declare(queue='temperature_queue', exclusive=False)
    queue_name = queue.method.queue

    channel.queue_bind(exchange='temperature_exchange', queue=queue_name, routing_key='temperature.*')

    conn = sqlite3.connect('temperatures.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temperatures (unit TEXT, value REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

    def callback(ch, method, properties, body):
        unit = method.routing_key.split('.')[-1]
        value = float(body)
        c.execute('INSERT INTO temperatures (unit, value) VALUES (?, ?)', (unit, value))
        conn.commit()
        print(f"Persisted {value} {unit}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    persist_temperature()