
# Ben Riesberg

# %% 
import os
import pandas as pd
import numpy as np 

from sec_api import QueryApi
from sec_api import ExtractorApi

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

#%% Set up working folder and test its existence
folder='C:/Users/brisb/fin510/Group Project'
exist=os.path.exists(folder)

#%% Pulls the 10ks for the stock and dates selected

queryApi = QueryApi(api_key="Insert your API Key here")
query = {
  "query": { "query_string": { 
      "query": "ticker:AAPL AND filedAt:{2017-01-01 TO 2022-04-01} AND formType:\"10-K\"" 
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

df =pd.json_normalize(filings['filings'])
df.drop(df[df['formType'] != '10-K'].index, inplace= True)
df.reset_index

#%% Gathers all the item 7s into one data frame
extractorApi = ExtractorApi("Insert your API key here")
Final_10k=[]
for index in df.index:
     filing_url = df['linkToFilingDetails'][index]
     section_10k_item7 = extractorApi.get_section(filing_url, "7", "text")
     Final_10k.append(section_10k_item7)

# %% FUNCTION Text to Sentences using NLTK
def txt2sentence(txt):
    sentences = sent_tokenize(txt)
    df=pd.DataFrame(sentences)
    return df

# %% SENTIMENT ANALYSIS 
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

df_AAPL=pd.DataFrame()
for index in range(len(Final_10k)):
    df_sentence = txt2sentence(Final_10k[index])
    
    results=[]
    for index, row in df_sentence.iterrows():
        try:
            results.append(nlp(row[0]))
        except:
            print('COULD NOT READ A LINE')
            
    sentiment=0
    
    for i in results:
        if i[0]['label'] == 'neutral':
            sentiment=sentiment+0
        if i[0]['label'] == 'negative':
            sentiment=sentiment-1
        if i[0]['label'] == 'positive':
            sentiment=sentiment+1
            
    Filing_Date=['10/29/2012','10/30/2020','10/31/2019','11/5/2018','11/3/2017']
    
    AAPL = [{'Ticker':"AAPL",'Sentiment':sentiment}]
    df_AAPL=df_AAPL.append(pd.DataFrame(AAPL))

#%% ROLLING ALPHA
import seaborn
import statsmodels.formula.api as sm # module for stats models
import statsmodels.api as sm2
from statsmodels.iolib.summary2 import summary_col # module for presenting stats models outputs nicely
from statsmodels.regression.rolling import RollingOLS

#!pip install pandas_datareader
import pandas_datareader.data as web

AAPL_df = web.DataReader('AAPL', 'yahoo', start='2011-02-28', end='2022-02-28')

def price2ret(prices,retType='simple'):
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret

AAPL_df['Returns']= price2ret(AAPL_df[['Adj Close']])
AAPL_df = AAPL_df.dropna()    

ff_factors = pd.read_csv('C:/Users/brisb/fin510/Group Project/F-F_Research_Data_Factors_daily.csv')

ff_factors = ff_factors.drop(labels= range(0,22418), axis = 0)
ff_factors = ff_factors.drop(labels = [25187,25188], axis = 0)
ff_factors = ff_factors.reset_index()
ff_factors = ff_factors.set_index(ff_factors['Date'])
ff_factors = ff_factors.drop(columns=['Date'])
ff_factors = ff_factors.drop(labels = 'index', axis=1)
ff_factors.rename(columns = {'Mkt-RF':'MKT'}, inplace = True)
ff_factors['MKT'] = ff_factors['MKT']/100
ff_factors['SMB'] = ff_factors['SMB']/100
ff_factors['HML'] = ff_factors['HML']/100


AAPL_df = AAPL_df.set_index(ff_factors.index)
AAPL_ff_merged = pd.merge(AAPL_df,ff_factors,left_index= True, right_index= True)
AAPL_ff_merged['XsRet'] = AAPL_ff_merged['Returns']-AAPL_ff_merged['RF']

endog = AAPL_ff_merged['XsRet']
exog = sm2.add_constant(AAPL_ff_merged['MKT'])
rols = RollingOLS(endog, exog, window=30)
rres = rols.fit()
params = rres.params.copy()
params.index = np.arange(1, params.shape[0] + 1)
params.head()
params= params.set_index(ff_factors.index)
params.rename(columns={'const':'Alpha'}, inplace= True)

params['Index'] = params.index
params['Index'] = range(1, len(params) + 1)
params.set_index('Index')


alpha2017=params['Alpha'][1713]
alpha2018=params['Alpha'][1965]
alpha2019=params['Alpha'][2213]
alpha2020=params['Alpha'][2465]
alpha2021=params['Alpha'][2716]

Alpha_Scores=[alpha2021, alpha2020, alpha2019, alpha2018, alpha2017]

Filing_Date=['10/29/2021','10/30/2020','10/31/2019','11/5/2018','11/3/2017']
df_AAPL['Filing Date']=Filing_Date
df_AAPL['30 Days Avg Alpha']=Alpha_Scores


#%% 
# Running an OLS regression on the relationship between sentiment and 
# average alpha generated up to 30 days after the earnings release.

x = df_AAPL['Sentiment'].tolist()
y = df_AAPL['30 Days Avg Alpha'].tolist()

reg1 = sm2.OLS(x,y).fit()

print(df_AAPL)
print(reg1.summary())






            