from table import table_read
import numpy as np
import pandas as pd

def_thlookup(ta,tc,qc)
    
    ta = 35
    tc = 24
    
    CtoK = 273.15
    
    tc +=CtoK
    ta +=CtoK
    
    qdata = pd.datarame(
        columns = ['th','qh'])
    
        for j in range(0,length(th_list)):
            th = th_list[j]
            [qc,qh,code] = table_read(ta,tc,th)