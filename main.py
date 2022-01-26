from BondPricesDao import BondPricesDao
from BondPricesTransformer import BondPricesTransformer

RAW_BOND_PRICES_CSV_FILENAME = "CDNGovtBondPricesRaw.csv"
PROCESSED_BOND_PRICES_CSV_FILENAME = "CDNGovtBondPricesProcessed.csv"

def _get_processed_data():
    try:
        processed_data = BondPricesDao.get_csv_data(PROCESSED_BOND_PRICES_CSV_FILENAME)
    except:
        raw_data = BondPricesDao.get_csv_data(RAW_BOND_PRICES_CSV_FILENAME)
        transfomer = BondPricesTransformer(raw_data)
        processed_data = transfomer.process_raw_data()
        BondPricesDao.save_df_as_csv(processed_data, PROCESSED_BOND_PRICES_CSV_FILENAME)
    return processed_data

def main():
    processed_data = _get_processed_data()
    return

if __name__ == "__main__":
    main()