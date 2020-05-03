# CHX min available 260 K ~ -13 degC. Exoamdable by running more DeltaEC simulations. Do not go above AHX, open window instead in that case
# AHX range 293-363 ~ 20-90 degC
# HHX max available 600 K ~ 327 degC, min at onset limit. Expandable by running more DeltaEC simulations

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d, griddata

file = r'data short.xlsx'
lt = pd.read_excel(file)

c_to_k = 273.15

ta = 300
tc = 292
th = 500

def amb_interpolator(temps,q_l,q_s,Tamb):
    qs = np.array([q_l,q_s])
    qf = interp1d(temps,qs)
    q = qf(Tamb)
    return q

def second_interpolator(whichrows,Tcold,Thot):
    points = whichrows[['CHX','HHX']].to_numpy()
    qhs = whichrows['Q_HHX'].to_numpy()
    qcs = whichrows['Q_CHX'].to_numpy()
    qh = griddata(points,qhs,(Tcold,Thot),method='linear')
    qc = griddata(points,qcs,(Tcold,Thot),method='linear')
    return qh, qc

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
    return rows_l, rows_h, fl_lo, fl_hi, np.array(hx_interest)

# all error flags
fl_amb_outrange = (ta > max(lt['AHX'].to_numpy()) or ta < min(lt['AHX'].to_numpy()))
fl_chx_lo = tc < min(lt['CHX'].to_numpy())
fl_chx_hi = (ta-3 < tc)
fl_hhx_lo = th < min(lt['HHX'].to_numpy())
fl_hhx_hi = th > max(lt['HHX'].to_numpy())

if fl_amb_outrange or fl_chx_lo or fl_chx_hi or fl_hhx_lo or fl_hhx_hi:
    if fl_amb_outrange or fl_chx_lo or fl_hhx_hi:
        print('Input data outside available range, run DeltaEC!')
        # return [1e16,1e16]
    if fl_chx_hi:
        print('CHX near as ambient, open window idiot!')
        # return [-1,-1]
    else:
        print('Cannot onset')
        # return [0.,0.]
    
else:
    # AHX
    rows_al, rows_ah, fl_a_lo, fl_a_hi, Ts_a = HX_lister ('AHX',lt,ta) # returns AHX low and AHX hi boundaries
    qh_al, qc_al = second_interpolator(rows_al,tc,th)
    qh_ah, qc_ah = second_interpolator(rows_ah,tc,th)
    qh = amb_interpolator(Ts_a,qh_al,qh_ah,ta)
    qc = amb_interpolator(Ts_a,qc_al,qc_ah,ta)
    
    if qc<=0 or qh<=0:
        print('Cannot onset')
        return [0.,0.]
    else:
        return [qc,qh]
        
    
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
    
    row_alclhl, row_alclhh, row_alchhl, row_alchhh, row_ahclhl, row_ahclhh, row_ahchhl, row_ahchhh, fl_amb_outrange, fl_chx_lo, fl_chx_hi, fl_hhx_lo, fl_hhx_hi = array_generator (ta,tc,th)
    
    

