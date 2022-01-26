class RatesRecorder:
    def __init__(self):
        self.rates_curve_by_date = {}
    
    def record_rates_curve(self, date, x, y):
        self.rates_curve_by_date[date] = (x, y)
    
    def print_all_data(self):
        for date in self.rates_curve_by_date:
            print("Rates curve for ", date, " in <date, rate> pairs: ")
            print(list(zip(self.rates_curve_by_date[date][0], self.rates_curve_by_date[date][1])))
            print("=====================")