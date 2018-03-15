#import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import quandl
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

start = dt.datetime(2017, 3, 1)
end = dt.datetime(2018, 3, 2)

api_key = '' #Insert Quandl API Key Here
quandl.ApiConfig.api_key = api_key
symbol = "BCHARTS/BITSTAMPUSD"
#symbol = "BITFINEX/IOTUSD" #an alternate ticker (IOTA vs. BITCOIN)
service = 'quandl'

#prices = web.DataReader(symbol, service, start, end)['Close']  #Data Reader Method
quandl_url = 'https://www.quandl.com/api/v3/datasets/' + symbol + '/data.csv?api_key=' + api_key
prices = quandl.get(symbol) #alt we could do this as a read url call in Pandas
returns = prices['Weighted Price'].pct_change()
replace = np.zeros(2366)
returns = np.where(np.isnan(returns),replace,returns)
returns = np.where(np.isinf(returns),replace,returns) # here we are replace inf with 0, probably sub-optimal
threshold = 15000 #some target value you are interested in seeing the chances of hitting

#last_price = prices[-1]
last_price = prices.iloc[-1]['Weighted Price'] #for quandl, which returns a dataframe

#number of Simulations
num_simulations = 10000
num_days = 252

simulation_df = pd.DataFrame()
for x in range(num_simulations):
	count = 0
	daily_vol = returns.std() #wird nan vs. NaN issues. Also needs to be called as np.ranstd(returns)

	price_series = []

	price = last_price * (1 + np.random.normal(0, daily_vol)) #There are probably other formulas for drift we could be using
	price_series.append(price)

	for y in range(num_days):
		if count == 251:
			break
		price = price_series[count] * (1 + np.random.normal(0, daily_vol))
		price_series.append(price)
		count += 1

	simulation_df[x] = price_series

ends = simulation_df.iloc[:,-1]

fig = plt.figure()
fig.suptitle('Monte Carlo Simulation: ' + symbol)
plt.plot(simulation_df)
plt.axhline(y=last_price, color = 'r', linestyle = '-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()
plt.clf
plt.hist(ends)
plt.show()

over_threshold = ends[ends <= threshold]
chances = len(ends[over_threshold]) / len(ends)

print("The chanes of exeding the selected threshold price are "+ str(chances))
