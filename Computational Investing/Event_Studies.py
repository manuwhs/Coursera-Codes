import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import functions as fu
import Homework1_func as H1

plt.close("all")

PLOT_GRAPHS = 0
#plt.clf()

allocation = [0.3,0.1,0.3,0.1,0.2]
symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]  
start_date = [2010, 1, 1]
end_date = [2010, 12, 31]
keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

# Get the metrics of the initial portfolio
H1.simulate_Portfolio(start_date, end_date, symbols,keys, allocation)

# Optimize porfolio
N_random = 100
best_Allocation = H1.optimize_Portfolio(start_date, end_date, symbols, keys,N_random)
H1.simulate_Portfolio(start_date, end_date, symbols,keys, best_Allocation)

# Plot efficiency frontier
N_random = 10000
best_Allocation = H1.plot_efficient_frontier(start_date, end_date, symbols, keys,N_random)







