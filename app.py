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
        f'api/v1.0/precipitation')


@app.route("api/v1.0/precipitation")

if __name__ == "__main__":
    app.run(debug=True)