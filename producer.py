import json
import time
import requests
from confluent_kafka import Producer

# OpenWeatherMap API configuration
API_KEY = "938ed07164d5a16b57896f59c0edff19"
CITY = "Warsaw"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Kafka configuration
KAFKA_TOPIC = "weather-data"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

# Kafka delivery callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [partition {msg.partition()}]")

# Main loop: fetch weather every 1 minute
print("Weather producer started. Sending data every 1 minute...")

while True:
    try:
        # Request current weather data
        response = requests.get(URL)
        if response.status_code != 200:
            print(f"Error fetching weather data: {response.status_code}")
            time.sleep(60)
            continue

        data = response.json()

        weather = {
            "city": CITY,
            "temp": round(data["main"]["temp"], 2),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": time.time()
        }

        print(f"Sending weather data: {weather}")
        producer.produce(KAFKA_TOPIC, json.dumps(weather).encode('utf-8'), callback=delivery_report)
        producer.flush()

    except Exception as e:
        print(f"Exception: {e}")

    # Wait 1 minute before the next request
    time.sleep(60)
