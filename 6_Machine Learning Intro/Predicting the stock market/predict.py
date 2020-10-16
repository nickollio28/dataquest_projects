'''
In this project I will be working with data from the S&P500 Index. I will use this dataset to develop a 
predictive model, training the model with data from 1950 to 2012, and testing the model with data from
2013 to 2015. 

'''

import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = pd.read_csv('sphist.csv', parse_dates = ['Date'])
data = data.sort_values('Date') # sort by ascending dates

# Calculate 5 day average closing price and standard deviation
# shift by 1 to not include current date - allows model to work in 'real world'
# 5 days because approx. 5 trading days per week
data['close_week_mean'] = data.Close.rolling(5).mean().shift(1)
data['close_week_std'] = data.Close.rolling(5).std().shift(1)

# Calculate volume 5 day avg & std
data['vol_week_mean'] = data.Volume.rolling(5).mean().shift(1)
data['vol_week_std'] = data.Volume.rolling(5).std().shift(1)


# Calculate 20 day average closing price and standard deviation
# 20 days because approx. 20 trading day per month
data['close_month_mean'] = data.Close.rolling(20).mean().shift(1)
data['close_month_std'] = data.Close.rolling(20).std().shift(1)

# Calculate volume 20 day avg & std
data['vol_month_mean'] = data.Volume.rolling(20).mean().shift(1)
data['vol_month_std'] = data.Volume.rolling(20).std().shift(1)

# Calculate 251 day average closing price and standard deviation
# 251 because approx. 251 trading days per year according to
# https://tradingsim.com/blog/trading-days-in-a-year/
data['close_year_mean'] = data.Close.rolling(251).mean().shift(1)
data['close_year_std'] = data.Close.rolling(251).std().shift(1)

# Calculate volume 251 day avg & std
data['vol_year_mean'] = data.Volume.rolling(251).mean().shift(1)
data['vol_year_std'] = data.Volume.rolling(251).std().shift(1)


# Drop null values
# First 251 rows where there wasn't enough data to calculate year_mean and year_std
data = data.dropna(axis=0)

# Use 2013-01-01 as date to begin testing
test_date = dt.datetime(year=2013, month=1, day=1)
train = data[data['Date'] < test_date]
test = data[data['Date'] >= test_date]

# Only use new columns as features
features = [i for i in data.columns if i.endswith('mean') or i.endswith('std')]
target = 'Close'

lr = LinearRegression()
lr.fit(train[features], train[target])
predictions = lr.predict(test[features])
rmse = mean_squared_error(predictions, test[target])**(1/2)

print('Root Mean Squared Error: ', rmse)
# Output: Root Mean Squared Error:  22.24912756194984