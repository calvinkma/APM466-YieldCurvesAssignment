from datetime import datetime, date
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

class RatesResullts:
    def __init__(self):
        self.rates_curve_by_date = {}
    
    def record_rates_curve(self, date, x, y):
        sorted_x, sorted_y = zip(*sorted(zip(x, y)))
        self.rates_curve_by_date[date] = (sorted_x, sorted_y)
    
    def print_all_data(self):
        for date in self.rates_curve_by_date:
            print("Rates curve for ", date, " in <date, rate> pairs: ")
            print(list(zip(self.rates_curve_by_date[date][0], self.rates_curve_by_date[date][1])))
            print("=====================")
    
    def plot(self, title, xlabel, ylabel, out_filename):
        cmap = plt.cm.get_cmap("BuPu")
        colors = cmap(np.linspace(0, 1, len(self.rates_curve_by_date)))

        for date, color in zip(self.rates_curve_by_date, colors):
            sorted_x, sorted_y = self.rates_curve_by_date[date][0], self.rates_curve_by_date[date][1]

            # Convert datetype x values to float-valued POXIS timestamp for interpolation
            sorted_x_sec = self._date_to_second(sorted_x)
            tck = interpolate.splrep(sorted_x_sec, sorted_y)

            # Define intermediate x values where the rate should be estimated
            sorted_x_sec_interpolated = np.linspace(sorted_x_sec[0], sorted_x_sec[-1], 500)
            sorted_x_interpolated = self._second_to_date(sorted_x_sec_interpolated)
            sorted_y_interpolated = interpolate.splev(sorted_x_sec_interpolated, tck)

            plt.plot(sorted_x_interpolated, sorted_y_interpolated, c=color)
            plt.plot(sorted_x, sorted_y, c=color, marker='x', linestyle='None', label='_nolegend_')
        
        plt.legend(self.rates_curve_by_date, ncol=3, labelspacing=0.05)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(out_filename)
    
    def _date_to_second(self, dates):
        return [datetime.combine(i, datetime.min.time()).timestamp() for i in dates]
    
    def _second_to_date(self, seconds):
        return [date.fromtimestamp(second) for second in seconds]
