# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 20:53:25 2022

@author: benri
"""
import pandas as pd
import numpy as np 

import statsmodels.formula.api as sm # module for stats models
from statsmodels.iolib.summary2 import summary_col # module for presenting stats models outputs nicely

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

#%%
def price2ret(prices,retType='simple'):
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret

# %%
def assetPriceReg(df_stk):
    import pandas_datareader.data as web # module for reading datasets directly from the web
    
    # Reading in factor data
    df_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench')[0]
    df_factors.rename(columns={'Mkt-RF': 'MKT'}, inplace=True)
    df_factors['MKT'] = df_factors['MKT']/100
    df_factors['SMB'] = df_factors['SMB']/100
    df_factors['HML'] = df_factors['HML']/100
    df_factors['RMW'] = df_factors['RMW']/100
    df_factors['CMA'] = df_factors['CMA']/100
    
    
    df_stock_factor = pd.merge(df_stk,df_factors,left_index=True,right_index=True) # Merging the stock and factor returns dataframes together
    df_stock_factor['XsRet'] = df_stock_factor['Returns'] - df_stock_factor['RF'] # Calculating excess returns

    # Running CAPM, FF3, and FF5 models.
    CAPM = sm.ols(formula = 'XsRet ~ MKT', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF3 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF5 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML + RMW + CMA', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})

    CAPMtstat = CAPM.tvalues
    FF3tstat = FF3.tvalues
    FF5tstat = FF5.tvalues

    CAPMcoeff = CAPM.params
    FF3coeff = FF3.params
    FF5coeff = FF5.params

  ##  DataFrame with coefficients and t-stats
    results_df = pd.DataFrame({'CAPMcoeff':CAPMcoeff,'CAPMtstat':CAPMtstat,
                               'FF3coeff':FF3coeff, 'FF3tstat':FF3tstat,
                               'FF5coeff':FF5coeff, 'FF5tstat':FF5tstat},
    index = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

    dfoutput = summary_col([CAPM,FF3, FF5],stars=True,float_format='%0.4f',
                  model_names=['CAPM','FF3','FF5'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'Adjusted R2':lambda x: "{:.4f}".format(x.rsquared_adj)}, 
                             regressor_order = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

    print(dfoutput)
    return results_df


#%% 
## THIS PULLS DATA FROM YAHOO FOR THE STOCKS IN LIST
Stocks=['AAPL','COKE','GOOGL','JPM','NVDA']
Stock_Data=[]
import pandas_datareader.data as web
for Stock in Stocks:
    temp_df = web.DataReader(Stock, 'yahoo', start='2021-03-01', end='2022-03-01')
    Stock_Data.append(temp_df)

## THIS RUNS CAPM/FAMA FRENCH MODEL ON ALL STOCKS
Reg_Output=[]
for df in Stock_Data:
    df['Returns']= price2ret(df[['Adj Close']])
    temp_df=assetPriceReg(df)
    Reg_Output.append(temp_df)
 
## THIS SEPERATES THE LIST OF DATA FRAMES TO INDIVIDUAL RESULTS    
AAPL_Results=Reg_Output[0]
COKE_Results=Reg_Output[1]
GOOGL_Results=Reg_Output[2]
JPM_Results=Reg_Output[3]
NVDA_Results=Reg_Output[4]
 
#%% Conclusions
# I was suprised to see that the FF 5 factor model had the highest R^2 across each company.  With all of the attention that the CAPM gets in academics, I assumed it would perform better.
# I was confused when I saw how poorly the models performed on COKE.  I noticed that the MKT P-Value on COKE is much smaller than the MKT P-Value for other stocks. 
# This makes sense because of the non-cyclicality of COKE
# Most of my stocks had positive Alpha's even if most of them were extremely close to 0.  
# JPM did have a negative Alpha across all models but that tracks with the low interest rate environment we are observing in markets.
# COKE had the highest alpha of any of my stocks.  This suprised me because the last year has been a good year for growth stocks. I thought AAPL or GOOGL would have a higher alpha.
# As we increased the number of variables, the R^2 went up across each study.  
#That doesnt necessarily make it a better study, but the P-Values can help us build a better model if they are considered to be significant.

#%% 
## EXPORTS DATA TO EXCEL FILE WITH EACH STOCK ON DIFFERENT SHEET
with pd.ExcelWriter(fullDir+'CAPM_FF_Output.xlsx') as writer:
    AAPL_Results.to_excel(writer, sheet_name="AAPL", index=False)
    COKE_Results.to_excel(writer, sheet_name="COKE", index=False)
    GOOGL_Results.to_excel(writer, sheet_name="GOOGL", index=False)
    JPM_Results.to_excel(writer, sheet_name="JPM", index=False)
    NVDA_Results.to_excel(writer, sheet_name="NVDA", index=False)