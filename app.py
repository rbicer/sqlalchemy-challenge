#IMPORT DEPENDICIES
import pandas as pd
import numpy as np
import datetime as dt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base


# Setup the Database 
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Show the Classes
Station = Base.classes.station
Measurement = Base.classes.measurement

#Session Creation
session = Session(engine)

#Set up Flask
app = Flask(__name__)

# FLASK ROUTES
     
@app.route("/")
def climate():
    return (
        f"The Climate Analysis of Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"The list of the Stations: /api/v1.0/stations<br/>"
        f"The list of the Precipitations: /api/v1.0/precipitation<br/>"
        f"The list of the tobs: /api/v1.0/tobs<br/>"
        f"The list of the Temperatures: /api/v1.0/temp/start/end"
    )
#Route for Stations
@app.route("/api/v1.0/stations")
def stations():
    """List of stations."""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Route for Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """The precipitation data!"""
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Route for tobs for previous year
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """The temperature observations (tobs)!"""

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

#Route for Temps
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """TMIN, TAVG, TMAX."""
    # Select 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run(debug=True)
