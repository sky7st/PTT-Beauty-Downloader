import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import twstock


stockId = input()

stock = twstock.realtime.get(stockId)

if stock['success'] == True:
    print(type(stock))
else:
    print(stock['rtmessage'])