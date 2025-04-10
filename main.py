import pandas as pd

from solar_energy_forecast.preprocess import get_data

#Yahli the king
def main():
    df = get_data(verbose=True)
    df.to_csv("output/complete_data.csv")


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    main()
