from Globals import Globals
from util import build_bond_cf

from datetime import datetime

class YieldCalculator:
    def __init__(self, data):
        self.data = data
    
    def get_yield_curve_on_date(self, string_date):
        yield_x, yield_y = [], []
        for _, row in self.data.iterrows():
            buy_date = datetime.strptime(string_date, Globals.DATETIME_FORMAT_STR).date()
            maturity_date = datetime.strptime(row["Maturity"], Globals.DATETIME_FORMAT_STR).date()

            cf = build_bond_cf(Globals.FACE_VALUE, buy_date, row[string_date], \
                               Globals.CPN_UNIT, row["Cpn"], Globals.NEXT_CPN_DATE, Globals.CPN_INTERVAL, \
                               maturity_date)
            
            # Calculate IRR
            ytm = 0

            yield_x.append(maturity_date)
            yield_y.append(ytm)
        
        return yield_x, yield_y
    