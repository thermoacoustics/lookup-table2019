def table_read(ta,tc,th):
    import pandas as pd
    import numpy as np
    from scipy.interpolate import RegularGridInterpolator

    file = r'data short.xlsx'
    lt = pd.read_excel(file)
    
    # ta = 293.
    # tc = 290.
    # th = 400.
    
    ahx_interest = []
    chx_interest = []
    hhx_interest = []
    
    # AHX
    ahx_list     = lt['AHX'] # locate the AHX range and values
    ahx_list     = ahx_list.drop_duplicates(keep='first')
    ahx_interest = ahx_list.iloc[(ahx_list-ta).abs().argsort()[:2]].sort_index().values.tolist() # find the two closest AHX values  
    rows         = lt[lt['AHX'].isin(ahx_interest)]
    
    # CHX
    chx_list     = lt['CHX'] # locate the AHX range and values
    chx_list     = chx_list.drop_duplicates(keep='first')
    chx_interest = chx_list.iloc[(chx_list-tc).abs().argsort()[:2]].sort_index().values.tolist()
    rows         = rows[rows['CHX'].isin(chx_interest)]
    
    # HHX
    hhx_list     = lt['HHX'] # locate the AHX range and values
    hhx_list     = hhx_list.drop_duplicates(keep='first')
    hhx_interest = hhx_list.iloc[(hhx_list-th).abs().argsort()[:2]].sort_index().values.tolist()
    rows         = rows[rows['HHX'].isin(hhx_interest)]
    
    # transform the 2x2x2 matrix to a interpolatble format qh_mat(ta,tc,th)
    qh_mat = np.zeros((len(ahx_interest),len(chx_interest),len(hhx_interest)))
    qc_mat = np.zeros((len(ahx_interest),len(chx_interest),len(hhx_interest)))
    
    for i in range(len(ahx_interest)):
        for j in range(len(chx_interest)):
            for k in range(len(hhx_interest)):
                qh_mat[i,j,k] = rows[(rows['AHX']==ahx_interest[i]) & (rows['CHX']==chx_interest[j]) & (rows['HHX']==hhx_interest[k])]['Q_HHX'].to_numpy()
                qc_mat[i,j,k] = rows[(rows['AHX']==ahx_interest[i]) & (rows['CHX']==chx_interest[j]) & (rows['HHX']==hhx_interest[k])]['Q_CHX'].to_numpy()
    
    qh = RegularGridInterpolator((ahx_interest,chx_interest,hhx_interest), qh_mat)(np.array([ta,tc,th]))[0]
    qc = RegularGridInterpolator((ahx_interest,chx_interest,hhx_interest), qc_mat)(np.array([ta,tc,th]))[0]

    return [qc,qh]