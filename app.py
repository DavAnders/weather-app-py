import os
import requests
import psycopg2
from psycopg2 import sql
from flask import Flask, render_template, request, jsonify
from datetime import date
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

conn = psycopg2.connect(DATABASE_URL)

def create_table():
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(50),
                country VARCHAR(50),
                temperature DECIMAL,
                description VARCHAR(100),
                date DATE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

create_table()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400
    
    try:
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}")
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("error", {})
                            .get("message", "Failed to fetch weather data")}), response.status_code
        
        weather = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_f"], # in fahrenheit
            "description": data["current"]["condition"]["text"],
            "date": date.today()
        }

        with conn.cursor() as cur:
            # Weather table must be created before running this code
            cur.execute("INSERT INTO weather (city, country, temperature, description) VALUES (%s, %s, %s, %s)",
                        (weather["city"], weather["country"], weather["temperature"], weather["description"]))
            conn.commit()

        return jsonify(weather)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)))