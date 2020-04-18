# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd


file = r'data short.xlsx'
lt = pd.read_excel(file)
#print(lt['AHX'])

#ta = float(input('AHX T = '))
#tc = float(input('CHX T = '))
#th = float(input('HHX T = '))
ta = 295.
tc = 256.
th = 405.

ahx_list = lt['AHX'] # locate the AHX range and values
ahx_list.drop_duplicates(keep='first',inplace=True)
ahx_interest = ahx_list.iloc[(ahx_list-ta).abs().argsort()[:2]].values.tolist() # find the two closest AHX values

