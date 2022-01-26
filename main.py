from datetime import datetime
from BondPricesDao import BondPricesDao
from BondPricesTransformer import BondPricesTransformer
from RatesRecorder import RatesRecorder
from YieldCalculator import YieldCalculator
from util import get_date_like_column_names
from Globals import Globals

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

    yield_rates_recorder = RatesRecorder()
    yield_calculator = YieldCalculator(processed_data)

    price_observation_string_dates = get_date_like_column_names(processed_data)
    for string_date in price_observation_string_dates:
        date = datetime.strptime(string_date, Globals.DATETIME_FORMAT_STR).date()
        yield_x, yield_y = yield_calculator.get_yield_curve_on_date(string_date)
        yield_rates_recorder.record_rates_curve(date, yield_x, yield_y)
    
    # Plot
    yield_rates_recorder.print_all_data()

    return

if __name__ == "__main__":
    main()