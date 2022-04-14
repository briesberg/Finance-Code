#i. What was the sentiment(s) Positive/Negative/Neutral?
#       The only stock that I had with a negative sentiment was AAPL.  JP Morgans sentiment score was exactly 0 which I thought was interesting.  
#ii. Stock performance after the disclosures?
#       I included red lines on my plots so stock performance could be assessed post 
#       earnings calls.  That said, positive sentiment often was reflected in positive returns in that period and vice versa.
#iii. What did you learn and what you would like to investigate deeper?
#       You could do this with other sections of the 10k but instead of sentiment 
#       analysis you could process the financials automatically and look for surprises in monitored ratios.

#%%

#!pip install sec_api
from sec_api import QueryApi
from sec_api import ExtractorApi
import pandas as pd
import numpy as np

#%%
queryApi = QueryApi(api_key="insert API Key Here")

query = {
  "query": { "query_string": { 
      "query": "ticker:AAPL AND filedAt:{2016-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  
  }
query_2 ={
  "query": { "query_string": { 
      "query": "ticker:COKE AND filedAt:{2016-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_3 ={
  "query": { "query_string": { 
      "query": "ticker:GOOGL AND filedAt:{2016-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_4 ={
  "query": { "query_string": { 
      "query": "ticker:JPM AND filedAt:{2016-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_5 ={
  "query": { "query_string": { 
      "query": "ticker:NVDA AND filedAt:{2016-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_6 ={
    "query": { "query_string": { 
        "query": "ticker:VOOG AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"N-CSR\"" 
      } }
    ,
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }
query_7 ={
    "query": { "query_string": { 
        "query": "ticker:VOOV AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"N-CSR\"" 
      } }
    ,
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }

queries = pd.read_csv("C:/Users/benri/FIN 510/10k- api work/Query list.csv")

filings_aapl = queryApi.get_filings(query)
df_aapl = pd.json_normalize(filings_aapl['filings']) 

filings_coke = queryApi.get_filings(query_2)
df_coke = pd.json_normalize(filings_coke['filings'])
filings_googl = queryApi.get_filings(query_3)
df_googl = pd.json_normalize(filings_googl['filings'])
df_googl = df_googl.drop([1,5])
df_googl = df_googl.reset_index()
df_googl = df_googl.drop(columns=('index'))

filings_jpm = queryApi.get_filings(query_4)
df_jpm = pd.json_normalize(filings_jpm['filings'])
filings_nvda = queryApi.get_filings(query_5)
df_nvda = pd.json_normalize(filings_nvda['filings'])

#filings_voog = queryApi.get_filings(query_6)
#df_voog = pd.json_normalize(filings_voog['filings'])
#filings_voov = queryApi.get_filings(query_7)
#df_voov = pd.json_normalize(filings_voov['filings'])

filing_url_aapl = df_aapl['linkToFilingDetails'].to_frame()
filing_url_coke = df_coke['linkToFilingDetails'].to_frame()
filing_url_googl = df_googl['linkToFilingDetails'].to_frame()
filing_url_jpm = df_jpm['linkToFilingDetails'].to_frame()
filing_url_nvda = df_nvda['linkToFilingDetails'].to_frame()
#filing_url_voog = df_voog['linkToFilingDetails'].to_frame()
#filing_url_voov = df_voov['linkToFilingDetails'].to_frame()

all_dfs = [filing_url_aapl, filing_url_coke, filing_url_googl, filing_url_jpm, filing_url_nvda]


df_all = pd.concat(all_dfs).reset_index(drop=True)

#%%

final_10k = []

for url in df_all.index:
     extractorApi = ExtractorApi("Insert API Key Here")
     section_10k_item7 = extractorApi.get_section(df_all['linkToFilingDetails'][url],"7",'text')
     final_10k.append(section_10k_item7)



def txt2sentence(txt):
    import nltk
    nltk.download('punkt')
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(txt, language= "english")
    df=pd.DataFrame(sentences)
    return df  



#pip install transformers
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')  

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

#%% 

sentiment = 0  
sentiment_df = pd.DataFrame()

for index in range(len(final_10k[0:4])):
    df_sentence = txt2sentence(final_10k[index])
    results = []
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('Could not read a line')

       
    
    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment = sentiment+0
        if i[0]['label']== 'negative':
            sentiment = sentiment-1
        if i[0]['label']== 'positive':
            sentiment = sentiment+1
    
aapl = [{'Ticker': 'AAPL','Year':'2016-2020','Sentiment score':sentiment}]
sentiment_df= sentiment_df.append(aapl)
print(aapl)
results = results.clear()
#%%
sentiment = 0  

for index in range(len(final_10k[5:9])):
    df_sentence = txt2sentence(final_10k[index+5])
    results = []
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('Could not read a line')
        
        

    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment = sentiment+0
        if i[0]['label']== 'negative':
            sentiment = sentiment-1
        if i[0]['label']== 'positive':
            sentiment = sentiment+1
    
coke = [{'Ticker': 'COKE','Year':'2016-2020','Sentiment score': sentiment}]
sentiment_df= sentiment_df.append(coke)
print(coke)
results = results.clear()
#%%
sentiment = 0

for index in range(len(final_10k[10:14])):
    df_sentence = txt2sentence(final_10k[index+10])
    results = []
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('Could not read a line')
        
       

    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment = sentiment+0
        if i[0]['label']== 'negative':
            sentiment = sentiment-1
        if i[0]['label']== 'positive':
            sentiment = sentiment+1
    
googl = [{'Ticker': 'GOOGL','Year':'2016-2020','Sentiment score': sentiment}]
sentiment_df= sentiment_df.append(googl)
print(googl)
results = results.clear()
#%%
sentiment = 0

for index in range(len(final_10k[15:19])):
    df_sentence = txt2sentence(final_10k[index+15])
    results = []
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('Could not read a line')
        
        

    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment = sentiment+0
        if i[0]['label']== 'negative':
            sentiment = sentiment-1
        if i[0]['label']== 'positive':
            sentiment = sentiment+1
    
jpm = [{'Ticker': 'JPM','Year':'2016-2020','Sentiment score': sentiment}]
sentiment_df= sentiment_df.append(jpm)
print(jpm)
results = results.clear()
#%%

sentiment = 0

for index in range(len(final_10k[20:25])):
    df_sentence = txt2sentence(final_10k[index+20])
    results = []
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('Could not read a line')
        
        

    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment = sentiment+0
        if i[0]['label'] == 'negative':
            sentiment = sentiment-1
        if i[0]['label'] == 'positive':
            sentiment = sentiment+1
    
nvda = [{'Ticker': 'NVDA','Year':'2016-2020','Sentiment score': sentiment}]
sentiment_df= sentiment_df.append(nvda)
print(nvda)
results = results.clear()

#%%

ticker = ['AAPL','COKE','GOOGL','JPM','NVDA']

def price2ret(prices, retType='simple'):
    if retType == 'simple':
        ret=(prices/prices.shift(1))-1
    else:
        ret=np.log(prices/prices.shift(1))
    return ret

import pandas_datareader as web 

AAPL_Price= web.DataReader('AAPL', 'yahoo', start='2015-01-01', end='2022-04-13')
AAPL_Price['Returns']= price2ret(AAPL_Price[['Adj Close']])

COKE_Price= web.DataReader('COKE', 'yahoo', start='2015-01-01', end='2022-04-13')
COKE_Price['Returns']= price2ret(COKE_Price[['Adj Close']])

GOOGL_Price= web.DataReader('GOOGL', 'yahoo', start='2015-01-01', end='2022-04-13')
GOOGL_Price['Returns']= price2ret(GOOGL_Price[['Adj Close']])

JPM_Price= web.DataReader('JPM', 'yahoo', start='2015-01-01', end='2022-04-13')
JPM_Price['Returns']= price2ret(JPM_Price[['Adj Close']])

NVDA_Price= web.DataReader('NVDA', 'yahoo', start='2015-01-01', end='2022-04-13')
NVDA_Price['Returns']= price2ret(NVDA_Price[['Adj Close']]) 
    


#%%

import matplotlib.pyplot as plt
from datetime import datetime

plt.figure()
plt.plot(AAPL_Price['Adj Close'], color='Black',)
plt.xlabel('Date')
plt.ylabel('Price')
plt.axvline(x=[datetime(2021,10,29)],color='Red')
plt.axvline(x=[datetime(2020,10,30)],color='Red')
plt.axvline(x=[datetime(2019,10,31)],color='Red')
plt.axvline(x=[datetime(2018,11,5)],color='Red')
plt.axvline(x=[datetime(2017,11,3)],color='Red')
plt.title('AAPL Price')

plt.figure()
plt.plot(AAPL_Price['Returns'], color='Black',)
plt.xlabel('Date')
plt.ylabel('% Returns')
plt.axvline(x=[datetime(2021,10,29)],color='Red')
plt.axvline(x=[datetime(2020,10,30)],color='Red')
plt.axvline(x=[datetime(2019,10,31)],color='Red')
plt.axvline(x=[datetime(2018,11,5)],color='Red')
plt.axvline(x=[datetime(2017,11,3)],color='Red')
plt.title('AAPL Returns')


plt.figure()
plt.plot(COKE_Price['Adj Close'], color='Black',)
plt.xlabel('Date')
plt.ylabel('Price')
plt.axvline(x=[datetime(2021,2,26)],color='Red')
plt.axvline(x=[datetime(2020,2,25)],color='Red')
plt.axvline(x=[datetime(2019,2,27)],color='Red')
plt.axvline(x=[datetime(2018,2,28)],color='Red')
plt.axvline(x=[datetime(2017,3,14)],color='Red')
plt.title('COKE Price')

plt.figure()
plt.plot(COKE_Price['Returns'], color='Black',)
plt.xlabel('Date')
plt.ylabel('% Returns')
plt.axvline(x=[datetime(2021,2,26)],color='Red')
plt.axvline(x=[datetime(2020,2,25)],color='Red')
plt.axvline(x=[datetime(2019,2,27)],color='Red')
plt.axvline(x=[datetime(2018,2,28)],color='Red')
plt.axvline(x=[datetime(2017,3,14)],color='Red')
plt.title('COKE Returns')


plt.figure()
plt.plot(GOOGL_Price['Adj Close'], color='Black',)
plt.xlabel('Date')
plt.ylabel('Price')
plt.axvline(x=[datetime(2021,2,3)],color='Red')
plt.axvline(x=[datetime(2020,2,4)],color='Red')
plt.axvline(x=[datetime(2019,2,5)],color='Red')
plt.axvline(x=[datetime(2018,2,6)],color='Red')
plt.title('GOOGL Price')

plt.figure()
plt.plot(GOOGL_Price['Returns'], color='Black',)
plt.xlabel('Date')
plt.ylabel('% Returns')
plt.axvline(x=[datetime(2021,2,3)],color='Red')
plt.axvline(x=[datetime(2020,2,4)],color='Red')
plt.axvline(x=[datetime(2019,2,5)],color='Red')
plt.axvline(x=[datetime(2018,2,6)],color='Red')
plt.title('GOOGL Returns')


plt.figure()
plt.plot(JPM_Price['Adj Close'], color='Black',)
plt.xlabel('Date')
plt.ylabel('Price')
plt.axvline(x=[datetime(2021,1,15)],color='Red')
plt.axvline(x=[datetime(2020,1,14)],color='Red')
plt.axvline(x=[datetime(2019,1,15)],color='Red')
plt.axvline(x=[datetime(2018,1,12)],color='Red')
plt.axvline(x=[datetime(2017,1,13)],color='Red')
plt.title('JPM Price')

plt.figure()
plt.plot(JPM_Price['Returns'], color='Black',)
plt.xlabel('Date')
plt.ylabel('% Returns')
plt.axvline(x=[datetime(2021,1,15)],color='Red')
plt.axvline(x=[datetime(2020,1,14)],color='Red')
plt.axvline(x=[datetime(2019,1,15)],color='Red')
plt.axvline(x=[datetime(2018,1,12)],color='Red')
plt.axvline(x=[datetime(2017,1,13)],color='Red')
plt.title('JPM Returns')


plt.figure()
plt.plot(NVDA_Price['Adj Close'], color='Black',)
plt.xlabel('Date')
plt.ylabel('Price')
plt.axvline(x=[datetime(2021,2,26)],color='Red')
plt.axvline(x=[datetime(2020,2,20)],color='Red')
plt.axvline(x=[datetime(2019,2,21)],color='Red')
plt.axvline(x=[datetime(2018,2,28)],color='Red')
plt.axvline(x=[datetime(2017,3,1)],color='Red')
plt.title('NVDA Price')

plt.figure()
plt.plot(NVDA_Price['Returns'], color='Black',)
plt.xlabel('Date')
plt.ylabel('% Returns')
plt.axvline(x=[datetime(2021,2,26)],color='Red')
plt.axvline(x=[datetime(2020,2,20)],color='Red')
plt.axvline(x=[datetime(2019,2,21)],color='Red')
plt.axvline(x=[datetime(2018,2,28)],color='Red')
plt.axvline(x=[datetime(2017,3,1)],color='Red')
plt.title('NVDA Returns')

#%%
print(sentiment_df)
