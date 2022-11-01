import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.pro-football-reference.com'
maxp = 300
df = []

for year in range(2010, 2022):
    print(str(year) + "\n")
    r = requests.get(url + "/years/" + str(year) + "/fantasy.htm")
    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]
    for i, row in enumerate(parsed_table.find_all('tr')[2:]):
        if i % 10 == 0:
            print(i, end=' ')
        if i >= maxp:
            print('\nComplete')
            break
        try:
            dat = row.find('td', attrs={'data-stat': 'player'})
            name = dat.a.get_text()
            stub = dat.a.get('href')
            stub = stub[:-4] + "/fantasy/" + str(year)
            pos = row.find('td', attrs={'data-stat': 'fantasy_pos'}).get_text()
            rec = row.find('td', attrs={'data-stat': 'rec'}).get_text()
            tdf = pd.read_html(url + stub)[0]
            tdf.columns = tdf.columns.get_level_values(-1)
            tdf = tdf.rename(columns={'Unnamed: 4_level_2': 'Away'})
            tdf['Away'] = [1 if r=='@' else 0 for r in tdf['Away']]
            # FanDuel Scoring system
            tdf = tdf.iloc[:,[1, 2, 3, 4, 5, -1]]
            tdf = tdf.query('Date != "Total"')
            tdf['Name'] = name
            tdf['Position'] = pos
            tdf['Season'] = year
            df.append(tdf.reset_index(drop=True))
        except:
            pass
df = pd.concat(df, ignore_index=True)
df.to_csv('fantasy_points.csv')
