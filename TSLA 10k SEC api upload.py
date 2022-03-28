# -*- coding: utf-8 -*-
#%%
from pathlib import Path
import sys
import os

home = str(Path.home())
print(home)

if sys.platform == 'linux':
    inputDir = '/FIN 510/API code/' 
elif sys.platform == 'win32':
    inputDir = '/FIN 510/API code/' 
else :
    inputDir = '/FIN 510/API code/'
fullDir = home+inputDir
print(fullDir)

import pandas as pd

tsla10k = pd.read_csv("C:/FIN510/API code/TSLA_10K_Dataframe.csv")


#%% To do this for a single 10k
#!pip install sec_api
from sec_api import ExtractorApi
# %% Very important: Register and get an api key!!!

extractorApi = ExtractorApi("insert your key here")


# extractorApi = ExtractorApi("")
# %% Tesla 10-K filing
filing_url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

# %% get the standardized and cleaned text of section 1A "Risk Factors"
section_text = extractorApi.get_section(filing_url, "7", "text")

# %% get the original HTML of section 7 "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
section_html = extractorApi.get_section(filing_url, "7", "html")

print(section_text)
##print(section_html)
#%% to do this for multiple 10k's
#!pip install sec_api


for link in tsla10k.index:
    filing_url = tsla10k["URL"][link]
   
    section_text = extractorApi.get_section(filing_url,"7", "text")
    print(tsla10k['Company'][link])
    print(tsla10k['Year'][link])
    print(section_text)
    # save the sections into your hard drive
    


