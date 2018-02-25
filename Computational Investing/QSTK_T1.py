import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import functions as fu
plt.close("all")

PLOT_GRAPHS = 0
#plt.clf()

ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]  
# SPX index of the S&P500 
# These are the securities, equities, assets, shares, however you want to call it.

dt_start = dt.datetime(2010, 1, 1)  # Start date we read the data
dt_end = dt.datetime(2010, 12, 31)  # End date we read the data
dt_timeofday = dt.timedelta(hours=16) # Day star date we read the data
# The reason we need to specify 16:00 hours is because we want to read the data that was available to us at the close of the day.

# Set the timestamp
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

#  Read the data from yahoo finance web
c_dataobj = da.DataAccess('Yahoo')  # Yahoo finance web, no yahoo stock
# Info we get from the Stock
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
# Get the data from the symbols
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
# Ldf_data is DATAFRAME !!!

# Now we want to access the data with the names of the keys so we convert it
# into a diccionary.
d_data = dict(zip(ls_keys, ldf_data))

shit_data = d_data["high"]["AAPL"][0:30]


""" CREATE FIGURE OF NORMALIZED PRICES """

# Get the price of the close values all the companies.
na_price = d_data['close'].values
na_normalized_price = na_price / na_price[0, :]

labels = ['Adjusted Close', "Days", 'Adjusted Close', ls_symbols]
if (PLOT_GRAPHS):
    fu.plot_graph(ldt_timestamps,na_normalized_price,labels, 1)


""" CREATE FIGURE OF RETURNS """
Returns = []
for symbol in ls_symbols:
    Returns.append(fu.get_Return(d_data['close'][symbol].values))
    
Returns = np.array(Returns).T

labels = ['Adjusted Close Returns', "Days", 'Adjusted Close', ls_symbols]
if (PLOT_GRAPHS):
    fu.plot_graph([],Returns,labels, 1)

""" SCATTER PLOT """


indx_1 = 0
indx_2 = 2

labels = ['Scatter Equities', ls_symbols[indx_1], ls_symbols[indx_2]]
if (PLOT_GRAPHS):
    fu.scatter_graph(Returns[:, indx_1],Returns[:, indx_2],labels, 1)


# Normalize prices




