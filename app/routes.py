from app import app
from app.core import engine
from flask import render_template
from flask import request
from datetime import datetime

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():

    # get any query param for the number of days between [5, 60] , defaulting to 30
    days = request.args.get('days', default=engine.DEFAULT_DAYS, type=int)
    if(days < 10 ):
        days = 10
    elif (days > 50):
        days = 50

    # generate graphs
    collectedInfo = engine.collectData(days)

    return render_template('index.html')