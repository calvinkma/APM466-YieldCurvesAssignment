from Globals import Globals
from util import build_bond_cf, calculate_irr

from datetime import datetime
from math import exp, log

class SpotCalculator:
    def __init__(self, data):
        self.data = data
    
    def get_spot_curve_on_date(self, string_date):
        buy_date = datetime.strptime(string_date, Globals.DATETIME_FORMAT_STR).date()
        spot_rate_by_end_date = {buy_date: 0}

        for _, row in self.data.iterrows():
            maturity_date = datetime.strptime(row["Maturity"], Globals.DATETIME_FORMAT_STR).date()

            cf = build_bond_cf(Globals.FACE_VALUE, buy_date, row[string_date], \
                               Globals.CPN_UNIT, row["Cpn"], Globals.NEXT_CPN_DATE, Globals.CPN_INTERVAL, \
                               maturity_date)
            
            last_pmt_date = cf[-1][0]
            last_pmt_amt = cf[-1][1]
            npv_last_pmt = (-1.0) * SpotCalculator._calculate_spot_curve_npv(cf[0:-1], buy_date, spot_rate_by_end_date)
            spot_rate_to_last_pmt_date = (-1.0) * log(npv_last_pmt / last_pmt_amt) / (last_pmt_date - buy_date).days * 365

            spot_rate_by_end_date[last_pmt_date] = spot_rate_to_last_pmt_date

        return spot_rate_by_end_date.keys(), spot_rate_by_end_date.values()
    
    def _calculate_spot_curve_npv(cf, today_date, spot_rate_by_end_date):
        """Calculate NPV of a cash flow using spot curve.

        Keywork arguments:
        cf -- A list of lists, each containing [date, value]
        today_date -- A date object representing today
        spot_rate_by_end_date -- A map of <DateTime end_date, Integer spot_rate>
        """
        npv = 0
        for date, value in cf:
            n_days = (date - today_date).days
            npv += value * exp((-1) * spot_rate_by_end_date[date] / 365.0 * n_days)
        
        return npv

            
    