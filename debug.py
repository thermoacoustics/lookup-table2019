# CHX min available 260 K ~ -13 degC. Exoamdable by running more DeltaEC simulations. Do not go above AHX, open window instead in that case
# AHX range 293-363 ~ 20-90 degC
# HHX max available 600 K ~ 327 degC, min at onset limit. Expandable by running more DeltaEC simulations

import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator, griddata

file = r'data short.xlsx'
lt = pd.read_excel(file)

c_to_k = 273.15

ta = 300
tc = 292
th = 320

def array_generator (Tamb,Tcool,Thot):
    def HX_lister (whichHX,inputlist,Temp):
        hx_interest = []
        # 
        hx_list     = inputlist[whichHX] # locate the AHX range and values
        hx_list     = hx_list.drop_duplicates(keep='first')
        hx_interest = hx_list.iloc[(hx_list-Temp).abs().argsort()[:2]].sort_index().values.tolist() # find the two closest AHX values
        fl_lo = Temp < min(hx_interest)
        fl_hi = Temp > max(hx_interest)
        rows_l = inputlist[inputlist[whichHX]==(hx_interest[0])]
        rows_h = inputlist[inputlist[whichHX]==(hx_interest[1])]
        return rows_l, rows_h, fl_lo, fl_hi
    
    
    # AHX
    rows_al, rows_ah, fl_a_lo, fl_a_hi = HX_lister ('AHX',lt,ta) # returns AHX low and AHX hi boundaries
    
    
        
    
    # CHX
    rows_alcl, rows_alch, fl_alc_lo, fl_alc_hi = HX_lister ('CHX',rows_al,tc) # AHX at lo boundary
    rows_ahcl, rows_ahch, fl_ahc_lo, fl_ahc_hi = HX_lister ('CHX',rows_ah,tc) 
    
    
    # HHX
    row_alclhl, row_alclhh, fl_alclh_lo, fl_alclh_hi = HX_lister ('HHX',rows_alcl,th)
    row_alchhl, row_alchhh, fl_alchh_lo, fl_alchh_hi = HX_lister ('HHX',rows_alch,th)
    row_ahclhl, row_ahclhh, fl_ahclh_lo, fl_ahclh_hi = HX_lister ('HHX',rows_ahcl,th)
    row_ahchhl, row_ahchhh, fl_ahchh_lo, fl_ahchh_hi = HX_lister ('HHX',rows_ahch,th)
    
    fl_amb_outrange = (fl_a_lo or fl_a_hi)
    fl_chx_lo = (fl_alc_lo   or fl_ahc_lo)
    fl_chx_hi = (fl_alc_hi   or fl_ahc_hi   or Tcool>Tamb)
    fl_hhx_lo = (fl_alclh_lo or fl_alchh_lo or fl_ahclh_lo or fl_ahchh_lo) # This not expected to be triggered at this stage as table linera interpolated down to 300K
    fl_hhx_hi = (fl_alclh_hi or fl_alchh_hi or fl_ahclh_hi or fl_ahchh_hi) # Data insufficient if this is triggered
    
    rows = pd.concat([row_alclhl, row_alclhh, row_alchhl, row_alchhh, row_ahclhl, row_ahclhh, row_ahchhl, row_ahchhh])
    
    return row_alclhl, row_alclhh, row_alchhl, row_alchhh, row_ahclhl, row_ahclhh, row_ahchhl, row_ahchhh, fl_amb_outrange, fl_chx_lo, fl_chx_hi, fl_hhx_lo, fl_hhx_hi

row_alclhl, row_alclhh, row_alchhl, row_alchhh, row_ahclhl, row_ahclhh, row_ahchhl, row_ahchhh, fl_amb_outrange, fl_chx_lo, fl_chx_hi, fl_hhx_lo, fl_hhx_hi = array_generator (ta,tc,th)

hhx_list     = rows['HHX'] # locate the AHX range and values
hhx_list     = hhx_list.drop_duplicates(keep='first')
hhx_interest = hhx_list.iloc[(hhx_list-th).abs().argsort()[:2]].sort_index().values.tolist()
fl_hhx_hi    = (th > max(hhx_interest))
fl_hhx_lo    = (th < min(hhx_interest))
rows         = rows[rows['HHX'].isin(hhx_interest)]

# use the return flags for output
# when not onset
# if fl_hhx_lo or fl_chx_hi:
#     if fl_hhx_lo:
#         print('HHX =', th, 'too low, minimum available', min(hhx_interest)) # when HHX outrange the table availability i.e.300K
#     elif fl_chx_hi:
#         print('CHX =', th, 'larger than ambient,', ta, 'open window instead') # when CHX is higher than ambient
#     return [0.,0.]
# elif fl_chx_lo or fl_hhx_hi or fl_ahx_outrange:
#     print('Undefined temperature range')
#     return [0.,0.]
# else:  
#     try:
#         # transform the 2x2x2 matrix to a interpolatble format qh_mat(ta,tc,th)
#         qh_mat = np.zeros((len(ahx_interest),len(chx_interest),len(hhx_interest)))
#         qc_mat = np.zeros((len(ahx_interest),len(chx_interest),len(hhx_interest)))
        
#         for i in range(len(ahx_interest)):
#             for j in range(len(chx_interest)):
#                 for k in range(len(hhx_interest)):
#                     qh_mat[i,j,k] = rows[(rows['AHX']==ahx_interest[i]) & (rows['CHX']==chx_interest[j]) & (rows['HHX']==hhx_interest[k])]['Q_HHX'].to_numpy()
#                     qc_mat[i,j,k] = rows[(rows['AHX']==ahx_interest[i]) & (rows['CHX']==chx_interest[j]) & (rows['HHX']==hhx_interest[k])]['Q_CHX'].to_numpy()
        
#         qh = RegularGridInterpolator((ahx_interest,chx_interest,hhx_interest), qh_mat)(np.array([ta,tc,th]))[0]
#         qc = RegularGridInterpolator((ahx_interest,chx_interest,hhx_interest), qc_mat)(np.array([ta,tc,th]))[0]
#         if qh>=0 and qc>=0:
#             return [qc,qh]
#         else:
#             print ('Not onset 1')
#             return [0.,0.]

#     except ValueError:
#         print ('Not onset')
#         return [0.,0.]
