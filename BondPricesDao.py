import pandas as pd

class BondPricesDao():    
    def get_csv_data(csv_filename):
        return pd.read_csv(csv_filename)

    def save_df_as_csv(df, csv_filename):
        df.to_csv(csv_filename, index=False)