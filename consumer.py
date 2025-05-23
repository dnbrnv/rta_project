from confluent_kafka import Consumer
import json
import joblib
import pandas as pd
import csv

# Load trained model (predicts actual indoor temperature based on external conditions)
model = joblib.load('model.pkl')

# Kafka config
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'weather-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['weather-data'])

print("Waiting for weather data... Press Ctrl+C to stop.")

# Comfort target logic
def recommend_temp(outdoor_temp):
    if outdoor_temp < 5:
        return 22.5
    elif outdoor_temp > 25:
        return 24.0
    else:
        return 21.5 + (outdoor_temp - 15) * 0.1

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Decode weather data
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Received: {data}")

        # Prepare data for model
        model_input = {
            'T_out': data['temp'],
            'RH_out': data['humidity'],
            'Windspeed': data['wind_speed']
        }
        df = pd.DataFrame([model_input])

        # Predict actual indoor temperature
        predicted_temp = model.predict(df)[0]

        # Get comfort recommendation
        recommended_temp = recommend_temp(data['temp'])

        # Decide action
        delta = recommended_temp - predicted_temp
        if delta > 1:
            action = "Turn on heating"
        elif delta < -1:
            action = "Turn on cooling"
        else:
            action = "No action needed"

        # Print results
        print(f"Predicted indoor: {predicted_temp:.2f}°C | Recommended: {recommended_temp:.2f}°C → {action}")

        # Save to CSV
        with open("climate_control_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                data['timestamp'],
                data['temp'],
                data['humidity'],
                data['wind_speed'],
                round(predicted_temp, 2),
                round(recommended_temp, 2),
                action
            ])

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    consumer.close()