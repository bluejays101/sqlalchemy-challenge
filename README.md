# 🌴 Hawaii Climate Analysis API 🌦️

## 📝 Project Description

This project builds a Flask-based web API to access climate data collected from weather stations in Hawaii.
The data was sourced from a SQLite database containing historical weather measurements and station information.

Users can interact with the API to retrieve precipitation data, station listings, temperature observations, and statistical temperature summaries through defined API routes.

---

## ⚙️ Installation and Setup Instructions

1. Clone or download this repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install required Python packages by running:
    ```
    pip install flask sqlalchemy
    ```
4. Note the `hawaii.sqlite` database file is located in directory called `Resources`.
5. Open a terminal, navigate to the project directory, and run:
    ```
    python app.py
    ```
6. Open a web browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

---

## 🛣️ Available API Routes

- `/`  
    Lists all available API routes.

- `/api/v1.0/precipitation`  
    Returns a JSON dictionary of dates and precipitation observations for the last 12 months.

- `/api/v1.0/stations`  
    Returns a JSON list of weather station IDs.

- `/api/v1.0/tobs`  
    Returns a JSON list of temperature observations (TOBS) for the most active station over the last 12 months.

- `/api/v1.0/<start>`  
    Returns a JSON list containing the minimum, average, and maximum temperatures for all dates greater than or equal to the provided start date.  
    Example: `/api/v1.0/2016-08-23`

- `/api/v1.0/<start>/<end>`  
    Returns a JSON list containing the minimum, average, and maximum temperatures for dates between the provided start and end dates inclusive.  
    Example: `/api/v1.0/2016-08-23/2017-08-23`

---

## 🛠️ Technologies Used

- Python 3.8+
- Flask
- SQLAlchemy
- SQLite
- Pandas (for initial data exploration)

---

## 🧠 Notes and Assumptions

- The dataset contains climate measurements up to August 23, 2017.  
  Queries beyond this date will return no results.
- Date inputs for `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` must follow the `YYYY-MM-DD` format.
- The API focuses on backend functionality only and returns data in JSON format.
- The application is designed to be lightweight and easily extendable.

---

## 📚 Example Usage

After starting the Flask server:

- Visit `http://127.0.0.1:5000/` to view available routes.
- Retrieve last year's precipitation data at `http://127.0.0.1:5000/api/v1.0/precipitation`.
- Retrieve list of weather stations at `http://127.0.0.1:5000/api/v1.0/stations`.
- Retrieve temperature observations for the most active station at `http://127.0.0.1:5000/api/v1.0/tobs`.

---
