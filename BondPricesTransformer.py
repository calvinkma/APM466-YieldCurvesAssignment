from datetime import datetime
import pandas as pd

class BondPricesTransformer:
    DATETIME_FORMAT_STR = "%m/%d/%Y"
    LAST_COUPON_DATE = datetime.strptime("9/1/2021", DATETIME_FORMAT_STR)


    def __init__(self, raw_data):
        self.data = raw_data
    
    def process_raw_data(self):
        self._filter_bonds()._adjust_bond_prices()
        return self.data
    
    def _filter_bonds(self):
        is_maturing_in_mar = self.data["Maturity"].str.contains("3/1/")
        mar_mature_bonds = self.data[is_maturing_in_mar]

        is_maturing_in_sep = self.data["Maturity"].str.contains("9/1/")
        sep_mature_bonds = self.data[is_maturing_in_sep]

        self.data = pd.concat([mar_mature_bonds, sep_mature_bonds])
        return self
    
    def _adjust_bond_prices(self):
        columns = list(self.data)
        price_observation_dates = list(filter(lambda x: x.count("/") == 2, columns))

        for date in price_observation_dates:
            self.data[date] = self.data.apply(lambda x: self._calculate_dirty_price(x, date), axis = 1)
        
        return self
    
    def _calculate_dirty_price(self, df_row, date):
        issue_date = datetime.strptime(df_row["Issue Date"], BondPricesTransformer.DATETIME_FORMAT_STR)
        accured_interest_starting_date = max(issue_date, BondPricesTransformer.LAST_COUPON_DATE)
        n_days_accured_interest = (datetime.strptime(date, BondPricesTransformer.DATETIME_FORMAT_STR) - accured_interest_starting_date).days
        return df_row[date] + n_days_accured_interest / 365.0 * df_row["Cpn"]

