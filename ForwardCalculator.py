from Globals import Globals
from util import date_to_second

from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import log

from scipy import interpolate

class ForwardCalculator:
    def __init__(self, spot_rates_results):
        self.spot_rates_results = spot_rates_results
    
    def get_1yr_forward_curve_on_date(self, string_agreement_date):
        forward_x, forward_y = [], []
        agreement_date = datetime.strptime(string_agreement_date, Globals.DATETIME_FORMAT_STR).date()
        spot_rate_1_year = self._get_n_year_spot_rate(agreement_date, agreement_date + relativedelta(years=1))

        for n_year_to_pmt in [2,3,4,5]:
            payment_date = agreement_date + relativedelta(years=n_year_to_pmt)
            spot_rate_n_year = self._get_n_year_spot_rate(agreement_date, payment_date)
            forward_rate = (log(spot_rate_n_year) - log(spot_rate_1_year)) / (n_year_to_pmt - 1) * (-1)
            forward_x.append(payment_date)
            forward_y.append(forward_rate)

        return forward_x, forward_y

    def _get_n_year_spot_rate(self, agreement_date, payment_date):
        tck = self.spot_rates_results.tck_by_date[agreement_date]
        pmt_date_in_seconds = date_to_second([payment_date])[0]
        return interpolate.splev(pmt_date_in_seconds, tck)

