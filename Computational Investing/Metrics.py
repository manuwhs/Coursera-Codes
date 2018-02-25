# -*- coding: utf-8 -*-
"""
u
"""
import functions as fu
import numpy as np
### LOADING FUNCTIONS ###

data = fu.load_dataset("./aapl.csv")
price = np.array(data["Close"]);

labels = ["Apple Price at Close", "Days", "Dollars"]
fu.plot_graph([],price,labels, 1)


Returns = fu.get_Return(price)
labels = ["Apple Return Price at Close", "Days", "%"]
fu.plot_graph([],Returns,labels, 1)

E_Return = np.mean(Returns)
std_Return = np.std(Returns)

SharpR = fu.get_SharpR(Returns)
SortinoR = fu.get_SortinoR(Returns)
print "Expected Dayly Return: " + str(E_Return)
print "STD of Return: " + str(std_Return)
print "Sharp Ratio: " + str(SharpR)
print "Sortino Ratio: " + str(SortinoR)