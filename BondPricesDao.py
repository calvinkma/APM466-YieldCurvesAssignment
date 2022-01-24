import pandas as pd

class BondPricesDao():
    BOND_PRICES_CSV_FILENAME = "CDNGovtBondPrices.csv"

    def __init__(self):
        self._load_csv()
        return
    
    def _load_csv(self):
        df = pd.read_csv(self.BOND_PRICES_CSV_FILENAME)
        print(df)
