
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import functions as fu

def get_Prices (start_date, end_date, symbols, keys):

    dt_start = dt.datetime(start_date[0], start_date[1], start_date[2])  # Start date we read the data
    dt_end = dt.datetime(end_date[0], end_date[1], end_date[2])  # End date we read the data
    dt_timeofday = dt.timedelta(hours=16) # Day star date we read the data
    
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    
    c_dataobj = da.DataAccess('Yahoo')  # Yahoo finance web, no yahoo stock
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, keys)
    d_data = dict(zip(keys, ldf_data))
    
    return d_data, ldt_timestamps

def get_Symbol_returns (d_data, key, symbols):
    Returns = []
    for symbol in symbols:
        Returns.append(fu.get_Return(d_data[key][symbol].values))
    Returns = np.array(Returns).T
    return Returns
    
def get_Portfolio_metrics(Returns, allocation):
  # Get the returns
    
    Total_Returns = Returns.dot(allocation)
    # Obtain the metrics for every symbol
    P_Cum_Ret = np.sum(Total_Returns)
    P_E_return = np.mean(Total_Returns)
    P_std_Return = np.std(Total_Returns)
    
    P_SharpR = fu.get_SharpR(Total_Returns)
    P_SortinoR = fu.get_SortinoR(Total_Returns)
    
    
    return P_E_return, P_Cum_Ret,P_std_Return ,P_SharpR ,P_SortinoR
    
def simulate_Portfolio(start_date, end_date, symbols,keys, allocation):
    # This function gets several data from your portfolio
    d_data, timestamps = get_Prices (start_date, end_date, symbols, keys)
    Returns = get_Symbol_returns (d_data, 'close', symbols)
    
    P_E_return, P_Cum_Ret,P_std_Return ,P_SharpR ,P_SortinoR = get_Portfolio_metrics(Returns, allocation)

    print "-------------------------------------------------------"
    print "Portfolio Metrics" 
    print "Allocation: " + str(allocation)
    print "Expected Daily Return: " + str(P_E_return)
    print "Cummulative Return: " + str(P_Cum_Ret)
    print "Volatily (std Return): " + str(P_std_Return)
    
    print "Sharp Ratio: " + str(P_SharpR)
    print "Sortino Ratio: " + str(P_SortinoR)
    print "-------------------------------------------------------"
    
def optimize_Portfolio(start_date, end_date, symbols, keys, Nrandom):
    # This function gets several data from your portfolio
    d_data, timestamps = get_Prices (start_date, end_date, symbols, keys)
    Returns = get_Symbol_returns (d_data, 'close', symbols)
    
    nSymbols = len(symbols)
    
    # Try random porfolios !!!

    Randoms = np.random.uniform(0,1,(Nrandom,nSymbols))
    Allocations = Randoms.T/np.sum(Randoms,1)  # Normalize to 1
    Allocations = Allocations.T
    Sharps_R = [];
    
    for i in range (Nrandom):
        P_E_return, P_Cum_Ret,P_std_Return ,P_SharpR ,P_SortinoR = get_Portfolio_metrics(Returns, Allocations[i,:])
        Sharps_R.append(P_SharpR)
    
    Sharps_R = np.array(Sharps_R)
    best_allocatio = np.argmax(Sharps_R)
    
    return Allocations[best_allocatio,:]
    

def plot_efficient_frontier(start_date, end_date, symbols, keys, Nrandom):
    # This function gets several data from your portfolio
    d_data, timestamps = get_Prices (start_date, end_date, symbols, keys)
    Returns = get_Symbol_returns (d_data, 'close', symbols)
    
    nSymbols = len(symbols)
    
    # Try random porfolios !!!

    Randoms = np.random.uniform(0,1,(Nrandom,nSymbols))
    Allocations = Randoms.T/np.sum(Randoms,1)  # Normalize to 1
    Allocations = Allocations.T
    P_Cum_Ret_s = [];
    P_std_Return_s = []
    for i in range (Nrandom):
        P_E_return, P_Cum_Ret,P_std_Return ,P_SharpR ,P_SortinoR = get_Portfolio_metrics(Returns, Allocations[i,:])
        P_Cum_Ret_s.append(P_Cum_Ret)
        P_std_Return_s.append(P_std_Return)
    
    P_std_Return_s = np.array(P_std_Return_s)
    P_Cum_Ret_s = np.array(P_Cum_Ret_s)
    
    # Obtain the metrics for every symbol
    Cum_Ret = np.sum(Returns,0)
    std_Return = np.std(Returns,0)
    
    labels = ['Porfolios', "Risk (std)", "Return"]
    
    fu.scatter_graph(P_std_Return_s,P_Cum_Ret_s,labels, 1)
    
    labels = ['Porfolios', "Risk (std)", "Return", ["Por","Eq"]]
    fu.scatter_graph(std_Return,Cum_Ret,labels, 0)
