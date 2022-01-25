from BondPricesDao import BondPricesDao
from BondPricesTransformer import BondPricesTransformer

def main():
    raw_data = BondPricesDao.get_raw_data()
    t = BondPricesTransformer(raw_data)
    return

if __name__ == "__main__":
    main()