from datetime import datetime
from math import log
import numpy as np

from BondPricesDao import BondPricesDao
from BondPricesTransformer import BondPricesTransformer
from RatesResults import RatesResults
from ForwardCalculator import ForwardCalculator
from YieldCalculator import YieldCalculator
from SpotCalculator import SpotCalculator
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

def _analyze_log_return_cov(rates_results, indices, output_filename):
    # Define matrix X with shape <n_variables, n_observations>
    # Each variable corresponds to an interest rate.
    # Each observation corresponds to the daily log return for everyday bond prices are recorded.
    bond_prices_record_dates = sorted(list(rates_results.rates_curve_by_date.keys()))
    n_observations = len(bond_prices_record_dates) - 1
    n_var = len(indices)

    X = np.zeros((n_var, n_observations))

    for var in range(n_var):
        for observation in range(n_observations):
            rate_after = rates_results.get_rate(bond_prices_record_dates[observation+1], indices[var])
            rate_before = rates_results.get_rate(bond_prices_record_dates[observation], indices[var])
            X[var, observation] = log(rate_after / rate_before)
    
    cov = np.cov(X)
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    idx = eigenvalues.argsort()[::-1]   
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]

    with open(output_filename, 'w') as f:
        print("Cov: \n", cov, file=f)
        print("Eigenvalues: \n", eigenvalues, file=f)
        print("Eigenvectors:: \n", eigenvectors, file=f)

def main():
    processed_data = _get_processed_data()

    yield_rates_results = RatesResults()
    yield_calculator = YieldCalculator(processed_data)

    spot_rates_results = RatesResults()
    spot_calculator = SpotCalculator(processed_data)

    price_observation_string_dates = get_date_like_column_names(processed_data)
    for string_date in price_observation_string_dates:
        date = datetime.strptime(string_date, Globals.DATETIME_FORMAT_STR).date()
        yield_x, yield_y = yield_calculator.get_yield_curve_on_date(string_date)
        yield_rates_results.record_rates_curve(date, yield_x, yield_y)

        spot_x, spot_y = spot_calculator.get_spot_curve_on_date(string_date)
        spot_rates_results.record_rates_curve(date, spot_x, spot_y)
    
    # Plot
    yield_rates_results.plot("CAN Govt Bond Yield Curve", "Maturity", "YTM", "yield_curves.png")
    spot_rates_results.plot("CAN Govt Bond Spot Curve", "End Date", "Spot Rate (Annual)", "spot_curves.png")

    # Forward rates requires interpolated spot rate values, and cannot be done before spot rate plots are generated.
    forward_rates_results = RatesResults()
    forward_calculator = ForwardCalculator(spot_rates_results)
    
    for string_date in price_observation_string_dates:
        date = datetime.strptime(string_date, Globals.DATETIME_FORMAT_STR).date()
        forward_x, forward_y = forward_calculator.get_1yr_forward_curve_on_date(string_date)
        forward_rates_results.record_rates_curve(date, forward_x, forward_y)

    forward_rates_results.plot("CAN Govt Bond 1yr Forward Curve", "End Date", "Forward Rate (Annual)", "forward_curves.png")

    # Calculate daily log returns
    _analyze_log_return_cov(yield_rates_results, range(1, 11, 2), 'daily_yield_rate_returns.txt')
    _analyze_log_return_cov(forward_rates_results, range(0, 4, 1), 'daily_future_rate_returns.txt')

    return

if __name__ == "__main__":
    main()