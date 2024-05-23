### Weather App Overview

The goal of this project is to gain a better understanding of Flask + PostgreSQL.

Flask handles server-side logic, while SQLAlchemy manages database interactions with PostgreSQL. Flask-Login ensures secure user authentication, and Flask-WTF with CSRF protection guards against web attacks. Flask-Migrate handles database changes, and the app integrates with WeatherAPI for real-time weather data.

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/DavAnders/weather-app-py
   cd weather-app-py
   ```

2. **Create a virtual environment and activate it:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root with the following content:

   ```plaintext
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://your_user:your_password@localhost:5432/weather_db
   API_KEY=your_weatherapi_key
   ```

5. **Initialize the database:**

   ```sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application:**

   ```sh
   flask run
   ```

## Usage

1. **Register an account:**

   - Go to `http://127.0.0.1:5000/register` and create a new account.

2. **Log in:**

   - Go to `http://127.0.0.1:5000/login` and log in with your credentials.

3. **Fetch weather data:**
   - Enter a city name in the input field and click "Get Weather" to fetch and display the current weather data for that city.
