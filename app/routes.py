from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from .models import db, UserWeather
from datetime import date
import requests
import os

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/api/weather', methods=['POST'])
@login_required
def get_weather():
    city = request.json.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    api_key = os.getenv('API_KEY')
    try:
        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}')
        data = response.json()

        if response.status_code != 200:
            return jsonify({'error': data.get('error', {}).get('message', 'Failed to fetch weather data')}), response.status_code

        weather = {
            'city': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country'],
            'temperature': data['current']['temp_f'], # in fahrenheit
            'description': data['current']['condition']['text'],
            'date': date.today()
        }

        user_weather = UserWeather(
            user_id=current_user.id,
            city=weather['city'],
            country=weather['country'],
            temperature=weather['temperature'],
            description=weather['description'],
            date=weather['date']
        )
        db.session.add(user_weather)
        db.session.commit()

        return jsonify(weather)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/weather/history', methods=['GET'])
@login_required
def get_weather_history():
    city = request.args.get("city")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not city or not start_date or not end_date:
        return jsonify({"error": "City, start_date, and end_date are required"}), 400

    try:
        history = UserWeather.query.filter_by(user_id=current_user.id, city=city).filter(UserWeather.date.between(start_date, end_date)).all()
        history_data = [
            {"city": item.city, "country": item.country, "temperature": item.temperature, "description": item.description, "date": item.date.isoformat()}
            for item in history
        ]
        return jsonify(history_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
