# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt 

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the existing database into new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    # Get the most recent date
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate the date 1 year ago from the most recent date
    query_start_date = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Get date and precipitation for the last year
    precip_data = session.query(Measurement.date, Measurement.prcp)\
                         .filter(Measurement.date >= query_start_date)\
                         .all()
    
    session.close()

    # Convert to dictionary
    precip_dict = {date: prcp for date, prcp in precip_data}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    # Get all station IDs
    station_data = session.query(Station.station).all()
    session.close()

    # Flatten list of tuples into normal list
    station_list = [station[0] for station in station_data]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    # Find the most active station
    most_active_station = session.query(Measurement.station)\
                                 .group_by(Measurement.station)\
                                 .order_by(func.count(Measurement.station).desc())\
                                 .first()[0]

    # Get the most recent date
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate date 1 year ago
    query_start_date = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the temperature observations for the most active station for the last year
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
                       .filter(Measurement.station == most_active_station)\
                       .filter(Measurement.date >= query_start_date)\
                       .all()
    
    session.close()

    # Convert to list of dictionaries
    tobs_list = [{date: temp} for date, temp in tobs_data]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end=None):
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end:
        # If end date is provided
        results = session.query(*sel)\
                         .filter(Measurement.date >= start)\
                         .filter(Measurement.date <= end)\
                         .all()
    else:
        # If no end date, search from start date to the most recent
        results = session.query(*sel)\
                         .filter(Measurement.date >= start)\
                         .all()

    session.close()

    # Unpack results
    temp_stats = list(results[0])
    return jsonify(temp_stats)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
