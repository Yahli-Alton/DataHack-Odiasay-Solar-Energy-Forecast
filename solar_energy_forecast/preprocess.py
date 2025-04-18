import glob

import pandas as pd


def get_data(verbose: bool = False) -> pd.DataFrame:
    df_pv = get_pv_data(verbose)
    df_solar = get_solar_data(verbose)
    df_weather = get_weather_data(verbose)
    df = df_pv.join(df_solar, how='inner').join(df_weather, how='inner')
    if verbose:
        print("\n## Complete Dataset:")
        print(df.info())
    return df


def get_weather_data(verbose: bool = False) -> pd.DataFrame:
    df_weather = pd.read_csv("data/world_weather_online.csv")
    df_weather['date_time'] = pd.to_datetime(df_weather['date_time'])
    df_weather.set_index('date_time', inplace=True)
    if verbose:
        print("\n## Weather data:")
        print(round(df_weather.describe(percentiles=[0.5]).transpose(), 2))
    return df_weather


def get_solar_data(verbose: bool = False) -> pd.DataFrame:
    df_solar = pd.concat([pd.read_csv(f) for f in glob.glob("data/nrel_solar_irradiance/*.csv")], ignore_index=True)
    df_solar['date_time'] = pd.to_datetime(df_solar[['Year', 'Month', 'Day', 'Hour', 'Minute']])
    df_solar.drop(columns=['Year', 'Month', 'Day', 'Hour', 'Minute'], inplace=True)
    df_solar = df_solar.set_index('date_time').sort_index()
    if verbose:
        print("\n## Solar data:")
        print(round(df_solar.describe(percentiles=[0.5]).transpose(), 2))
    return df_solar


def get_pv_data(verbose: bool = False) -> pd.DataFrame:
    df_pv = pd.read_csv("data/PV_Output_Hannover_MA.csv")
    df_pv['date_time'] = pd.to_datetime(df_pv['Timestamp'], format="%b %d, %Y %I%p")
    df_pv.drop(columns=['Timestamp', 'City', 'County', 'State'], inplace=True)
    df_pv.rename(columns={'% Baseline': 'relative_power'}, inplace=True)
    df_pv.set_index('date_time', inplace=True)
    if verbose:
        print("\n## PV data:")
        print(df_pv.describe(percentiles=[0.5]).transpose())
    return df_pv
