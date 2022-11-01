import requests
import pandas as pd

url = 'https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year='
# Find the first year data is available
# for year in range(2021, 0, -1):
#         res = requests.get(url + str(year))
#         if not res.ok:
#             print("Error accessing year: ", str(year))
#             break

first_year = 2010
adps = []

for year in range(first_year, 2022):
    res = requests.get(url + str(year))
    try:
        adp = res.json()["players"]
        df = pd.DataFrame(adp, index=range(len(adp)))
        df["Season"] = year
        adps.append(df)
    except KeyError:
        print("Error in year: ", year)

adps_df = pd.concat(adps)
adps_df.to_csv("adps_2010_to_2021.csv")