import os
import smtplib
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd 
from pandas_datareader import data as pdr

email_address = 'My throwaway Gmail'
email_password = 'My throwaway Password'

msg = EmailMessage()


yf.pdr_override()
start= dt.datetime(2000,1,1)
now= dt.datetime.now()

stock = "AAPL"
Target_Price = 160

msg["Subject"] = "Alert on "+stock
msg["From"]= email_address
msg["To"] = 'my monitored Gmail'

alerted = False

while 1:
    df= pdr.get_data_yahoo(stock,start,now)
    currentClose = df['Adj Close'][-1]
    
    condition = currentClose>Target_Price
    
    if(condition and alerted ==False):
        alerted = True
        
        message = stock +" Has activated the alert price of " + str(Target_Price) +\
        "\nCurrent Price: "+str(currentClose)
        
        print(message)

        msg.set_content(message)
        
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(email_address,email_password)
            smtp.send_message(msg)
            
            print('completed')
            
            

