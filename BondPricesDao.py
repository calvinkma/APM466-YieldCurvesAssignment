import pandas as pd

class BondPricesDao():
    BOND_PRICES_CSV_FILENAME = "CDNGovtBondPrices.csv"
    
    def get_raw_data():
        return pd.read_csv(BondPricesDao.BOND_PRICES_CSV_FILENAME)
