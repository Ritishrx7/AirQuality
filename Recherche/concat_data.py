import time
import pandas as pd
import urllib

BASE_URL = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/"

years = ["2023", "2024"]
FILE_BASE_FORMAT = "FR_E2_"
specific_hours = ["00:00:00", "08:00:00", "16:00:00"]


def get_all_month(year, month):
    """Downloads all available daily data for a specific month and filters it for 3 specific hours."""
    url = f"{BASE_URL}/{year}/{FILE_BASE_FORMAT}{year}-{month}"
    df = pd.DataFrame()
    
    for i in range(1, 32):  # Loop through all possible days of the month
        # Format day with leading zero if needed
        day = f"{i:02d}"

        try:
            daily_df = pd.read_csv(f"{url}-{day}.csv", sep=";")
            
            # Filter rows to keep only the specific hours
            if 'Date de début' in daily_df.columns:
                # Convert 'Date de début' to datetime 
                daily_df['Heure'] = pd.to_datetime(daily_df['Date de début']).dt.time
                daily_df = daily_df[daily_df['Heure'].astype(str).isin(specific_hours)]
                daily_df = daily_df.drop(columns=['Heure'])  # Drop the temporary 'Heure' column

        except FileNotFoundError:
            print(f"FileNotFound: {url}-{day}.csv")
            continue
        except urllib.error.HTTPError:
            print(f"FileNotFound: {url}-{day}.csv")
            continue

        # Concatenate the daily data into the monthly DataFrame
        df = pd.concat([df, daily_df]).reset_index(drop=True)

    return df


def get_all_year(year):
    """Downloads all monthly data for a year and filters it."""
    df = pd.DataFrame()
    
    for i in range(1, 13):  # Loop through all months
        month = f"{i:02d}"  # Format month with leading zero if needed
        print(f"Downloading month: {i} of year {year}")
        monthly_df = get_all_month(year, month)
        
        # Concatenate the monthly data into the yearly DataFrame
        df = pd.concat([df, monthly_df]).reset_index(drop=True)

    return df


if __name__ == "__main__":
    # Create an empty DataFrame to hold data for both years
    combined_df = pd.DataFrame()

    # Loop through the years 2023 and 2024 and concatenate their data into one DataFrame
    for y in years:
        yearly_df = get_all_year(y)
        combined_df = pd.concat([combined_df, yearly_df]).reset_index(drop=True)

    # Save the combined DataFrame as a single CSV file for both years
    combined_df.to_csv("AirQuality_2023_2024.csv", index=False)