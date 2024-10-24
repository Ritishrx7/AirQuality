import time

import pandas as pd
import urllib

BASE_URL = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/"

years = ["2021", "2022", "2023", "2024"]

FILE_BASE_FORMAT = "FR_E2_"

# YYYY_MM_DD.csv


def get_all_month(year, month):
    """ """
    url = f"{BASE_URL}/{year}/{FILE_BASE_FORMAT}{year}-{month}"
    df = pd.DataFrame()
    for i in range(1, 32):

        # Because file format have 0 in front of number for days
        if i < 10:
            day = f"0{i}"
        else:
            day = i

        # try & catch because some files might be missing
        # & some months don't have 31 days
        try:
            daily_df = pd.read_csv(f"{url}-{day}.csv", sep=";")
        except FileNotFoundError:
            print(f"FileNotFound: {url}-{day}.csv")
            continue
        except urllib.error.HTTPError:
            print(f"FileNotFound: {url}-{day}.csv")
            continue

        # Concat df & daily
        # Reset index because concat extend indexes by default
        if df.shape[1] != daily_df.shape[1] and i != 1:
            print(f"Diff col : {daily_df.columns}")
        df = pd.concat([df, daily_df]).reset_index(drop=True)

    return df


def get_all_year(year):
    df = pd.DataFrame()
    for i in range(1, 13):
        # Because file format have 0 in front of number for days
        if i < 10:
            month = f"0{i}"
        else:
            month = i
        print(f"Downloading month: {i}")
        monthly_df = get_all_month(year, month)
        df = pd.concat([df, monthly_df]).reset_index(drop=True)

    return df


if __name__ == "__main__":
    # st = time.perf_counter()

    # df_2021 = get_all_year("2021")

    # end = time.perf_counter()

    # print(df_2021.shape)
    # print(df_2021.head())
    # print(f"Tot time take: {end-st:.3f}s")
    # memory_in_mb = df_2021.memory_usage(deep=True).sum() / (1024**2)
    # print(f"Final DataFrame size: {memory_in_mb:.2f} MB")

    for y in years:
        df = get_all_year(y)
        df.to_csv(f"AirQuality_{y}.csv")
