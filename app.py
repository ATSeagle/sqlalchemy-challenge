# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Generate engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# use auto_map base and reflect database schema
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to tables in sqlite file
Station= Base.classes.station
Measurement= Base.classes.measurement


# Create an app, being sure to pass __name__
app = Flask(__name__)



# 3. Define what to do when a user hits the index route
@app.route("/")
def home():

    return f"""Available Routes: <br/>
        <br/>
        /api/v1.0/precipitation <br/>
        /api/v1.0/stations <br/>
        /api/v1.0/tobs <br/>
        /api/v1.0/<enter start date> <br/>
        /api/v1.0/start/end <br/><br/>
        For /api/v1.0/start and /api/v1.0/start/end routes, date must be between 2010-01-01 and 2017-08-23. </br></br>
        Date must be written in YYYY-MM-DD format."""


@app.route("/api/v1.0/precipitation")
def precipitation():

    # create session link to database
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():

    # create session link to database
    session=Session(engine)
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    # create session link to database
    session = Session(engine)
    temp_obs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').filter(Measurement.station == "USC00519281").all()
    session.close

    temp_results= list(np.ravel(temp_obs))

    return jsonify(temp_results)

   
@app.route("/api/v1.0/<start>")
def start(start):

    # create session link to database
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close

    results_list = []
    for min_temp, max_temp, avg_temp in results:
        results_dict = {}
        results_dict["Minimum Temperature"] = min_temp
        results_dict["Maximum Temperature"] = max_temp
        results_dict["Average Temperature"] = avg_temp
        results_list.append(results_dict)

    return jsonify(results_list)


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):

    # create session link to database
    session= Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temp_results= list(np.ravel(results))

    return jsonify(temp_results)


if __name__ == "__main__":
    app.run(debug=True)
