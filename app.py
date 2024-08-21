import matplotlib
matplotlib.use('Agg') 
import flask
from flask import Flask, render_template, request, send_file, jsonify, render_template_string
from byDatesClass import byDates
import yfinance as yf
from datetime import datetime
import pandas as pd

app=Flask(__name__)

def init():
    print("initializing... ") 

################### Nav Buttons #######################
    
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/historicaldata')
def historical_data():
    return render_template('historicaldata.html')

@app.route('/stockcomparison')
def stock_comparison():
    return render_template('stockcomparison.html')

@app.route('/newsanalysis')
def news_analysis():
    return render_template('newsanalysis.html')

@app.route('/candlestickdetect')
def candlestick_detect():
    return render_template('candlestickdetect.html')

@app.route('/modelbuilder')
def model_builder():
    return render_template('modelbuilder.html')


############# Retrieve and Process Inputs from Historical Analysis ##################
@app.route('/submit_form',methods = ['POST'])
def retrieve_hist_inputs():
    #Set these to None as not all of these are always retrieved
    yearInput = None
    quarterInput = None
    monthInput = None
    startDateInput = None
    endDateInput = None

    #These are always collected from the first input box
    ticker = request.form['ticker']
    datatype = request.form['datatype']
    interval = request.form['interval']
    plotVol = request.form['plotVol']

    #These are always collected from the second input box
    frequency = request.form['frequency'+interval.capitalize()]
    intervalsBack = int(request.form['intervalsBack'+interval.capitalize()])

    #This should go into the choose my interval form
    interval_str = frequency + "_" + interval

    #These are not always collected but if the intervals year, quarter, or month is chosen, then they are
    if (interval == 'year' or interval == 'quarter' or interval == 'month'):
        yearInput = int(request.form['yearInput'+interval.capitalize()])
        quarterInput = int(request.form['quarterInput'])
        monthInput = int(request.form['monthInput'])
    #Same with these but for week and day
    elif (interval == 'week' or interval == 'day'):
        startDateInput = datetime.strptime(request.form['startDateInput'+interval.capitalize()],'%Y-%m-%d')
        endDateInput = datetime.strptime(request.form['endDateInput'+interval.capitalize()],'%Y-%m-%d')

    #Error Handling
    try:
    #Start using the byDates class here
        stock = yf.Ticker(ticker)

        hist = stock.history('max','1d')

        byDatesObj = byDates(hist,datatype)
        vol_df = None

        byDatesObj.choose_interval(interval_str,intervals_back = intervalsBack, year = yearInput, quarter = quarterInput, month = monthInput,start_datetime = startDateInput, end_datetime = endDateInput)
        if (plotVol == 'yes'):
            volObj = byDates(hist,"Volume")
            volObj.choose_interval(interval_str,intervals_back = intervalsBack, year = yearInput, quarter = quarterInput, month = monthInput,start_datetime = startDateInput, end_datetime = endDateInput)
            vol_df = volObj.return_df()

        image_base64 = byDatesObj.html_plotter(vol_df = vol_df ,y_label = datatype)

        return '<img src="data:image/png;base64,' + image_base64 + '">'
    except TypeError as e1:
        print(e1)
        return 'Invalid Date Range'
    except AttributeError as e2:
        return 'Ticker Not Found'
    
    except Exception as e:
        return 'Invalid Inputs'
    

@app.route('/submit_bar_form',methods = ['POST'])
def retrieve_bar_inputs():
    #Set these to None as not all of these are always retrieved
    yearInput = None
    quarterInput = None
    monthInput = None
    startDateInput = None
    endDateInput = None

    #These are always collected from the first input box
    #ticker = request.form['ticker']
    datatype = request.form['datatype']
    interval = request.form['interval']

    category = request.form['category']
    stat = request.form['stat']
    largest_smallest = bool(int(request.form['largest_smallest']))
    num_results = int(request.form['num_results'])

    #plotVol = request.form['plotVol']

    #These are always collected from the second input box
    frequency = request.form['frequency'+interval.capitalize()]
    intervalsBack = int(request.form['intervalsBack'+interval.capitalize()])

    #This should go into the choose my interval form
    interval_str = frequency + "_" + interval

    #These are not always collected but if the intervals year, quarter, or month is chosen, then they are
    if (interval == 'year' or interval == 'quarter' or interval == 'month'):
        yearInput = int(request.form['yearInput'+interval.capitalize()])
        quarterInput = int(request.form['quarterInput'])
        monthInput = int(request.form['monthInput'])
    #Same with these but for week and day
    elif (interval == 'week' or interval == 'day'):
        startDateInput = datetime.strptime(request.form['startDateInput'+interval.capitalize()],'%Y-%m-%d')
        endDateInput = datetime.strptime(request.form['endDateInput'+interval.capitalize()],'%Y-%m-%d')

    #Error Handling
    try:
    #Start using the byDates class here
        #stock = yf.Ticker(ticker)
        
        #Can just use a blank dataframe to intiate the byDates class object
        hist = pd.DataFrame() #stock.history('max','1d')

        byDatesObj = byDates(hist,datatype)

        image_base64 = byDatesObj.bar_plotter(category = category, stat = stat, largest_smallest=largest_smallest ,num_results=num_results,datatype=datatype,interval_str=interval_str,intervals_back=intervalsBack ,year=yearInput, quarter=quarterInput, month=monthInput ,start_datetime=startDateInput, end_datetime=endDateInput)

        return '<img src="data:image/png;base64,' + image_base64 + '">'
    except TypeError as e1:
        #print(e1)
        return 'Invalid Date Range'
    except AttributeError as e2:
        return 'Ticker Not Found'
    
    except Exception as e:
        return 'Invalid Inputs'





if __name__ == '__main__':
    init()
    app.run(host = '0.0.0.0',debug=True, port=9090)
