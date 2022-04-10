# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 18:35:35 2022

@author: benri
"""

#Part I:
#Instructor's github: github.com/CinderZhang¶
#My github:
#Part II: Working with SEC Filing
#Following the step in Homework 2,
#a. Using Python, download 10Ks (5 years if available) of those stocks;
#b. Using Python, download N-CSR of the funds (1 or 2 funds, exclude index funds) which hold the stocks of interest;
#c. Parse the 10Ks and extract MD&A and any other section(s) you may need;
#d. Perform sentiment analysis on the sections;
#e. Perform sentiment analysis from N-CSR of the stock;
#f. Analysis the stock performance and write up of your findings.
#i. What was the sentiment(s) Positive/Negative/Neutral?
#ii. Stock performance after the disclosures?
#iii. What did you learn and what you would like to investigate deeper?



#!pip install sec_api
from sec_api import QueryApi
from sec_api import ExtractorApi
import pandas as pd


queryApi = QueryApi(api_key="insert api key here")

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


filing_url_aapl = df_aapl['linkToFilingDetails'].to_frame()
filing_url_coke = df_coke['linkToFilingDetails'].to_frame()
filing_url_googl = df_googl['linkToFilingDetails'].to_frame()
filing_url_jpm = df_jpm['linkToFilingDetails'].to_frame()
filing_url_nvda = df_nvda['linkToFilingDetails'].to_frame()
all_dfs = [filing_url_aapl, filing_url_coke, filing_url_googl, filing_url_jpm, filing_url_nvda]

number_list = list(range(1,11))

df_all = pd.concat(all_dfs).reset_index(drop=True)

#%%

for url in df_all.index:
     extractorApi = ExtractorApi("insert api key here")
     section_10k_item7 = extractorApi.get_section(df_all['linkToFilingDetails'][url],"6",'text')
     print(section_10k_item7)
     with open('C:/Users/benri/FIN 510/10k- api work/TSLA_10k_item2.txt', "w") as f:
         f.write(section_10k_item7)
     
    
