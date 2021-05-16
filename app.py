import numpy as np
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)
app = Flask(__name__)
@app.route("/")
def home():
    return(f'The following routes are available;<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>')



@app.route("/api/v1.0/precipitation")
def prcp():
    import datetime as dt
    start_date = dt.datetime(2016,8,23)
    one_year = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= start_date).all()
    raindex = [{'Dates':rain[0], "Precipitation":rain[1]} for rain in one_year]
    session.close()
    return jsonify(raindex)


@app.route('/api/v1.0/stations')
def station_name():
    stations = session.query(station.station).all()
    station_list = [{"Station Name":station[0]}for station in stations]
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs_flask():
    import datetime as dt
    station_count = session.query(measurement.station,func.count(measurement.prcp)).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    start_obs = dt.datetime(2016,8,18)
    temp_obs = session.query(measurement.station, measurement.date, measurement.tobs).\
    filter(measurement.station==station_count[0][0], measurement.date>=start_obs).all()
    temp_list = [{"Station":temps[0], "Date":temps[1], "Temp (F)":temps[2]}for temps in temp_obs]
    return jsonify(temp_obs)

@app.route('/api/v1.0/<start>')
def starts(start):
    selected = session.query(measurement.station, measurement.date, measurement.tobs).\
    filter(measurement.date>=start).all()
    selected_list = [{"Station":temps[0], "Date":temps[1], "Temp (F)":temps[2]}for temps in temp_obs]
    return jsonify(selected_list)



if __name__ == "__main__":
    app.run(debug=True)

