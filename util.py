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