# =============================================================================
# # To use, from reverser import Th_lookup
# # input ta,tc, and required qc and it can find out Th required to achieve
# # the code it slow, each iteration takes 1-2s although parallalized
# =============================================================================

def Th_lookup(ta,tc,qc):
    from table import table_read
    import numpy as np
    import pandas as pd
    from scipy.interpolate import interp1d
    
    from joblib import Parallel, delayed
    import multiprocessing
    # use parallel computing to reduce time
    
    # ta = 32
    # tc = 22
    
    CtoK = 273.15
    
    qdata = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
    
    th_list = np.arange(round(300-CtoK,3),round(601-CtoK,3),1)
    
    # for j in range(0,length(th_list)):
        
    def rowsearch(amb,cool,hot):
        qcool,qh,code = table_read(amb,cool,hot,False)
        return [hot,qcool]
    
    num_cores = multiprocessing.cpu_count()
         
    results = Parallel(n_jobs=num_cores)(delayed(rowsearch)(ta,tc,th) for th in th_list)
    # parallelized this line for higher efficiency
    
    qdata = pd.DataFrame(results,columns = ['th','qc']).drop_duplicates(subset=['qc'],keep='last')

    
    if qc>max(qdata['qc']):
        print('Qc required too large and Th gt. than 300 K. Outside Table range or system not onset')
        return 0.
    else:
        qth = interp1d(qdata['qc'],qdata['th'])
        Th = round(float(qth(qc)),3)
        return Th