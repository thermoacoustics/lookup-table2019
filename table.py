# this tabl generates the Q for ONE UNIT
# it returns qc, qh as two separate values
# # # # # # #
# error codes:
# 1 - input data outside available range
# 2 - CHX is close to ambient, hence no cooling demand
# 3 - won't onset
# 0 - it works

def table_read(ta,tc,th):
    import pandas as pd
    import numpy as np
    from scipy.interpolate import interp1d, griddata
    
    file = r'data short.xlsx'
    lt = pd.read_excel(file)
    
    c_to_k = 273.15
    
    ta +=c_to_k
    tc +=c_to_k
    th +=c_to_k
    
    def amb_interpolator(temps,q_l,q_s,Tamb):
        qs = np.array([q_l,q_s])
        qf = interp1d(temps,qs)
        q = qf(Tamb)
        return float(q)
    
    def second_interpolator(whichrows,Tcold,Thot):
        points = whichrows[['CHX','HHX']].to_numpy()
        qhs = whichrows['Q_HHX'].to_numpy()
        qcs = whichrows['Q_CHX'].to_numpy()
        qh = griddata(points,qhs,(Tcold,Thot),method='cubic')
        qc = griddata(points,qcs,(Tcold,Thot),method='cubic')
        return float(qh), float(qc)
    
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
    fl_chx_hi = (ta < tc)
    fl_hhx_lo = th < min(lt['HHX'].to_numpy())
    fl_hhx_hi = th > max(lt['HHX'].to_numpy())
    
    if fl_amb_outrange or fl_chx_lo or fl_chx_hi or fl_hhx_lo or fl_hhx_hi:
        if fl_amb_outrange or fl_chx_lo or fl_hhx_hi:
            print('Input data outside available range, run DeltaEC!')
            return 0.,0.,1
        if fl_chx_hi:
            print('CHX near as ambient, open window idiot!')
            return 0.,0.,2
        else:
            print('Cannot onset')
            return 0.,0.,3
        
    else:
        # AHX
        rows_al, rows_ah, fl_a_lo, fl_a_hi, Ts_a = HX_lister ('AHX',lt,ta) # returns AHX low and AHX hi boundaries
        qh_al, qc_al = second_interpolator(rows_al,tc,th)
        qh_ah, qc_ah = second_interpolator(rows_ah,tc,th)
        qh = amb_interpolator(Ts_a,qh_al,qh_ah,ta)
        qc = amb_interpolator(Ts_a,qc_al,qc_ah,ta)
        
        if qc<=10 or qh<=10: # threshold 10W for values to return
            print('Cannot onset')
            return 0.,0.,3
        else:
            return qc,qh,0
