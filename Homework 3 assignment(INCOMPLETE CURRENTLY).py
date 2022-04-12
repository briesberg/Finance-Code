from sec_api import QueryApi
from sec_api import ExtractorApi
import pandas as pd


queryApi = QueryApi(api_key="9da9b5776ef77dad3732e5e9d839ef14b409d6c927739c4689520b43993637be")

query = {
  "query": { "query_string": { 
      "query": "ticker:AAPL AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  
  }
query_2 ={
  "query": { "query_string": { 
      "query": "ticker:COKE AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_3 ={
  "query": { "query_string": { 
      "query": "ticker:GOOGL AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_4 ={
  "query": { "query_string": { 
      "query": "ticker:JPM AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
    } }
  ,
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
  }
query_5 ={
  "query": { "query_string": { 
      "query": "ticker:NVDA AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:\"10-K\"" 
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
#df_googl = df_googl.drop([1,5])
#df_googl = df_googl.reset_index()
#df_googl = df_googl.drop(columns=('index'))

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
     extractorApi = ExtractorApi("9da9b5776ef77dad3732e5e9d839ef14b409d6c927739c4689520b43993637be")
     section_10k_item7 = extractorApi.get_section(df_all['linkToFilingDetails'][url],"7",'text')
     final_10k.append(section_10k_item7)

def txt2sentence(txt):
    import nltk
    nltk.download('punkt')
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(txt)
    df=pd.DataFrame(sentences)
    return df  

results=[]

for string in final_10k:
    for i in string:
        text = string
        df_sentence = txt2sentence(text)
        results.append(df_sentence)
        print(text)
  
