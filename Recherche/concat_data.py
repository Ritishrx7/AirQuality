import pandas as pd

BASE_URL = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/"

years = ["2021", "2022", "2023", "2024"]

FILE_BASE_FORMAT = "FR_E2"


def get_dataframe(url):
    df = pd.read_csv(url)
    return df
