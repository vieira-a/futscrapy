from cgi import print_environ
from lxml import etree
from cgitb import html, text
from typing import Text
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Open offline file
url = open('files/267/267.html', 'r')
html = url.read()
soup = BeautifulSoup(html, 'html.parser')
dom = etree.HTML(str(soup))

# Set div location for date and sold for filds; The divs has same pattern:
   # Complete XPath data field: /html/body/div[9]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[1]/text()
   # Complete XPath sold field: /html/body/div[9]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[1]/div[3]/text()

# Join strings to get path

path_count = 0
path_base = '/html/body/div[9]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[' 
path_data = ']/div[1]/text()'
path_sold = ']/div[3]/text()'

# Getting date and sold informations:
    # Get path in a range to date and sold fields
    # Get content with dom.xpath (get_data and get_sold)
    # Build a dict named transactions with the texts of the fields 

for i in range(100):
    path_count = path_count + 1
    path_data_all = path_base + str(path_count) + path_data
    path_sold_all = path_base + str(path_count) + path_sold
    
    get_data = dom.xpath(path_data_all)
    get_sold = dom.xpath(path_sold_all)

    if get_sold != [' 0 ']:
        
        transactions = {
            'data_sold': get_data,
            'sold_for': get_sold
        }
        
# Cleaning and formatting data strings
    # Slicing strings to get text
    # Clean text with replace

        transactions_str = str(transactions)
        month = (transactions_str[17:20])
        day = (transactions_str[20:23]).strip()
        year = 2022
        hour = (transactions_str[26:38])
        hour = hour.replace("'",'').replace(']', '').replace(',', '')
        sold = transactions_str[50:63].replace(',','.')
        sold = sold.replace("'",'').replace(']', '').replace(',', '').replace('[', '').replace('.000', '').strip()
    
        month_dt = datetime.datetime.strptime(month, '%b')
        month_num = month_dt.month
        date_num = (str(day)+'/'+str(month_num)+'/'+str(year))

    # Add 0 in beginning of the string to make all hours with 4 characters (ex. 01:00)
        hour_1 = (hour[0:3]).replace(':', '')
        hour_1 = int(hour_1)
        if hour_1 < 10:
            hour_1 = '0' + str(hour_1)
        hour_2 = hour[3:9].replace(':', '')
        hour = (str(hour_1) + ':' + str(hour_2)).strip()

    # Convert hour string in 24 time format    
        def convert24(hour):
            if hour[-2:] == "AM" and hour[:2] == "12":
                return "00" + hour[2:-2]

            elif hour[-2:] == "AM":
                return hour[:-2]
            
            elif hour[-2:] == "PM" and hour[:2] == "12":
                return hour[:-2]

            else:
                return str(int(hour[:2]) + 12) + hour[2:6]
        hour = convert24(hour).strip()

    # Build the final dict or CSV file to Pandas and data model
        transactions_dict = (date_num, hour, sold)
        print(transactions_dict)