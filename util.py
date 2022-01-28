from math import exp
import scipy.optimize as optimze

def get_date_like_column_names(df):
    columns = list(df)
    column_names = list(filter(lambda x: x.count("/") == 2, columns))
    return column_names

def build_bond_cf(face_val, buy_date, buy_price, \
                  cpn_rate, cpn_unit, next_cpn_date, cpn_interval, \
                  maturity_date):
    # Initial payment to purchase the bond
    cf = [[buy_date, (-1)*buy_price]]
    
    # Coupon payments
    cpn_date = next_cpn_date
    while cpn_date <= maturity_date:
        cf.append([cpn_date, face_val * cpn_rate * cpn_unit])
        cpn_date = cpn_date + cpn_interval
    
    # Add notional on the last coupon
    cf[-1][1] += face_val

    return cf

def get_constant_interest_npv(cf, today_date, r=0.01):
    """Calculate NPV of a cash flow assuming a constant interest rate.

    Keywork arguments:
    cf -- A list of lists, each containing [date, value]
    today_date -- A date object representing today
    r -- Annual interest rate, compounded continuously
    """

    npv = 0
    for date, value in cf:
        n_days = (date - today_date).days
        npv += value * exp((-1) * r / 365.0 * n_days)
    
    return npv

def calculate_irr(cf, today_date):
    """Calculate internal rate of return associated with a cash flow.
    """
    sol = optimze.root(lambda x: get_constant_interest_npv(cf, today_date, x), [0])
    
    if len(sol.x) != 1:
        print("Warn!!")
    return sol.x[0]
