# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:15:53 2022

@author: benri
"""

import pandas as pd
import numpy as np 
import seaborn
import statsmodels.formula.api as sm # module for stats models
import statsmodels.api as sm2
from statsmodels.iolib.summary2 import summary_col # module for presenting stats models outputs nicely
from statsmodels.regression.rolling import RollingOLS

# %%
from pathlib import Path
import sys
import os

home = str(Path.home())
print(home)

# %%
if sys.platform == 'linux':
    inputDir = '/FIN 510/Homework 2/' 
elif sys.platform == 'win32':
    inputDir = '/FIN 510/Homework 2/' 
else :
    inputDir = '/FIN 510/Homework 2/'
    
fullDir= home+inputDir
print(fullDir)

Stocks=['AAPL']


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


ff_factors = pd.read_csv('C:/Users/benri/FIN 510/Group Project Code/F-F_Research_Data_Factors_daily.csv')

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


























