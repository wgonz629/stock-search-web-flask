import functools
import requests
import json 
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import (
    Blueprint, flash, g, redirect, request, url_for
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/data', methods=["GET"])
def parseData():
    
    tiingo_api_token = '2e60e48782d8be49b0f9e7b9a3b627bc50bdc58d'
    tiingo_api_url = 'https://api.tiingo.com'

    news_api_url = 'https://newsapi.org/v2'
    news_api_token = '3a67c2b7713c47cf8e309fd9c1fc2b35'

    stock_symbol = request.args.get('stock_symbol')

    response = {}
    status_code = 200
    headers = {
        'Content-Type': 'application/json'
    }

    # Get the Company Outlook Tab Data
    
    # handle invalid/valid stock_symbol 
    route = f'{tiingo_api_url}/tiingo/daily/{stock_symbol}?token={tiingo_api_token}'
    
    requestRespone = requests.get(route, headers = headers)

    if(requestRespone.status_code == 200):
        companyOutlook = json.loads(requestRespone.text)
        response.update({'companyOutlook': companyOutlook})
    else:
        # break and return with status code 400
        status_code = 400
        response.update({
            'message': 'Error : No record has been found, please enter a valid symbol.'
        })
        return response, status_code

    # Get the data for Stock Summary Tab 

    route = f'{tiingo_api_url}/iex/?tickers={stock_symbol}&token={tiingo_api_token}'
    requestRespone = requests.get(route, headers = headers)
    stockSummary = json.loads(requestRespone.text)

    response.update({'stockSummary': stockSummary})

    # Get the stock price/volume chart data
    
    # startDate shoud be current date - six months
    six_months = date.today() + relativedelta(months=-6)
    startDate = six_months.strftime("%Y-%m-%d")
    
    route = f'{tiingo_api_url}/iex/{stock_symbol}/prices?startDate={startDate}&resampleFreq=12hour&columns=open,high,low,close,volume&token={tiingo_api_token}'
    requestRespone = requests.get(route, headers = headers)
    stockPrice = json.loads(requestRespone.text)
    date_closing = []
    date_volume = []
    for entry in stockPrice:
        _date = entry['date']
        _date = datetime.datetime.strptime(_date,"%Y-%m-%dT%H:%M:%S.%fZ")
        _date = _date.strftime("%s") 
        closingPrice = entry['close']
        volume = entry['volume']
        date_closing.append([int(_date)*1000, closingPrice])
        date_volume.append([int(_date)*1000, int(volume)])

    response.update({'stockPrice': {'date_closing': date_closing, 'date_volume': date_volume}})

    # Get stock news data 
    route = f'{news_api_url}/everything?apiKey={news_api_token}&q={stock_symbol}&pageSize=100'
    requestRespone = requests.get(route, headers = headers)
    newsDump = json.loads(requestRespone.text)['articles']

    newsArticles = []

    for news in newsDump:
        if(len(newsArticles) < 5):
            if(news['title'] != None and news['url'] != None and news['urlToImage'] != None and news['publishedAt'] != None ):
                data = {
                    'title': news['title'],
                    'url': news['url'],
                    'urlToImage': news['urlToImage'],
                    'publishedAt': news['publishedAt']
                }
                newsArticles.append(data)
    
    response.update({'news': newsArticles})

    return response, status_code