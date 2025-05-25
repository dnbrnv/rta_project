# rta_project
# Smart Climate Control System

A real-time intelligent climate simulation system that uses **live weather data** and a **machine learning model** to predict indoor temperature and recommend comfort adjustments.

---

## Project Goals

- Collect real-time weather data from OpenWeather API
- Predict indoor temperature using a trained regression model
- Recommend climate actions based on comfort rules
- Visualize temperature trends and system decisions in a dashboard

---

## Technologies Used

- **Python 3.12**
- `pandas`, `requests`, `scikit-learn`, `joblib`
- `confluent-kafka` for messaging
- `matplotlib`, `streamlit` for visualization
- **Apache Kafka + Zookeeper** (Docker)
- Dataset: [UCI Appliances Energy Prediction](https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction)

---

## Project Structure

- `producer.py` — fetches weather data from OpenWeather and sends it to Kafka every minute  
- `consumer.py` — consumes messages from Kafka, runs ML prediction, and logs actions  
- `train_model.py` — trains regression model using UCI energy dataset  
- `model.pkl` — trained regression model (stored with `joblib`)  
- `climate_control_log.csv` — log of all predictions and decisions  
- `visualizer.py` — Streamlit dashboard with temperature trends and actions  
- `.streamlit/config.toml` — enables dark theme for the dashboard  
- `docker-compose.yml` — runs Kafka and Zookeeper containers  
- `requirements.txt` — list of Python dependencies  
