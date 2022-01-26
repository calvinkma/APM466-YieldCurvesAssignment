from Globals import Globals
from util import get_date_like_column_names

from datetime import datetime
import pandas as pd

class BondPricesTransformer:
    LAST_COUPON_DATE = datetime.strptime("9/1/2021", Globals.DATETIME_FORMAT_STR).date()

    def __init__(self, raw_data):
        self.data = raw_data
    
    def process_raw_data(self):
        self._filter_bonds()._adjust_bond_prices()
        return self.data
    
    def _filter_bonds(self):
        is_maturing_in_mar_sep = self.data["Maturity"].str.match("(3\/1\/)|(9\/1\/)")
        self.data = self.data[is_maturing_in_mar_sep].copy()
        return self
    
    def _adjust_bond_prices(self):
        price_observation_dates = get_date_like_column_names(self.data)

        for date in price_observation_dates:
            dirty_prices = self.data.apply(lambda x: self._calculate_dirty_price(x, date), axis = 1)
            self.data.loc[:, date] = dirty_prices
        
        return self
    
    def _calculate_dirty_price(self, df_row, date):
        issue_date = datetime.strptime(df_row["Issue Date"], Globals.DATETIME_FORMAT_STR).date()
        accured_interest_starting_date = max(issue_date, BondPricesTransformer.LAST_COUPON_DATE)
        n_days_accured_interest = (datetime.strptime(date, Globals.DATETIME_FORMAT_STR).date() - accured_interest_starting_date).days
        return df_row[date] + n_days_accured_interest / (365.0 / 2) * df_row["Cpn"]

