import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
	return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():
    year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').\
        order_by(Measurement.date).all()
    return jsonify(year)



@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    stations = list(np.ravel(results))
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()
    temps = list(np.ravel(temp))
    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def startDateOnly(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    results = list(np.ravel(temp))
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)