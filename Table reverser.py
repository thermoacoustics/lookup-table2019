from table import table_read
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

from joblib import Parallel, delayed
import multiprocessing
# use parallel computing to reduce time

def thlookup(ta,tc,qc)
    
    ta = 35
    tc = 24
    
    CtoK = 273.15
    
    qdata = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
    
    th_list = np.arange(round(300-CtoK,3),round(601-CtoK,3),10)
    
    # for j in range(0,length(th_list)):
        
    def rowsearch(ta,tc,th):
        qc,qh,code = table_read(ta,tc,th,False)
        # qdata = qdata.append([th,qc], column = ['th','qc'], ignore_index=True)
        return [th,qc]
    
    num_cores = multiprocessing.cpu_count()
         
    results = Parallel(n_jobs=num_cores)(delayed(rowsearch)(ta,tc,th) for th in th_list)
    
    qdata = pd.DataFrame(results,columns = ['th','qh'])
    
    # [table_read(ta,tc,th,False) for th in th_list]