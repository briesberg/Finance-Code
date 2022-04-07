
#Based on this code I can conclude that the stock price is not stationary.

amzn <- read.csv('AMZN.csv')
amzn_Adj.Close <- ts(amzn$Adj.Close,frequency = 253, start = c(2010,1))
plot.ts(amzn$Adj.Close)

library(forecast)
library(TSstudio)

rho<-acf(amzn_Adj.Close,lag.max = 500)
prho<-pacf(amzn_Adj.Close,lag.max = 500)
print(rho)
print(prho)

#This code will be where I do the first order difference and recalculate ACF and PACF:
frst_ordr_dif  <- amzn$Adj.Close - amzn$Adj.Close.Lagged.1
plot.ts(frst_ordr_dif)

rho_frstordr_dif <- acf(frst_ordr_dif,lag.max = 50)
prho_frstordr_dif<- pacf(frst_ordr_dif,lag.max = 50)
print(rho_frstordr_dif)
print(prho_frstordr_dif)

fit1<-Arima(frst_ordr_dif,order = c(1,0,0))
#print(fit1)

fit2<-Arima(frst_ordr_dif,order = c(0,1,1))
#print(fit2)

fit3<-Arima(frst_ordr_dif,order = c(0,0,1))
#print(fit3)

fit4<-Arima(frst_ordr_dif,order = c(1,0,1))
#print(fit4)

fit5<-auto.arima(frst_ordr_dif)
#print(fit5)

checkresiduals(fit1)
res<-residuals(fit1)


library(lmtest)
Box.test(residuals(fit4),lag = 4,type = "Ljung-Box")


#install.packages("Hmisc")
library("Hmisc")

reg1 <- lm(formula = amzn$Adj.Close~amzn$Adj.Close.Lagged.1,data = amzn)
summary(reg1)


#Creating an index for our for loop, then using the for loop to do our forecast:

y=1:253
yhat=1:253
yhat_rw=1:253

#Rolling Window
for(i in 1:253){
  fit_loop<-Arima(frst_ordr_dif[i:2261+i-1],order = c(1,0,1))
  #print(fit_loop)
  fcst_loop<-Arima(frst_ordr_dif[2261+i-1],model=fit_loop)
  yhat[i]<- fitted(fcst_loop)
  yhat_rw[i]<-frst_ordr_dif[2261+i-1]
  y[i]<-frst_ordr_dif[2261+i]
  #print(i)
  #print(y)
  #print(yhat)
  #print(yhat_rw)
}

yhat%>%
  accuracy(y)

yhat_rw%>%
  accuracy(y)





