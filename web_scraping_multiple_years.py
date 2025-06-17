import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_1902():
    url = 'https://www.baseball-almanac.com/yearly/yr1902a.shtml'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        b_tag = p.find('b')
        if b_tag:
            stat = b_tag.get_text(strip=True).replace(':', '')
            full_text = p.get_text(strip=True)
            rest = full_text[len(stat)+1:].strip()

            parts = rest.rsplit(' ', 1)
            if len(parts) == 2 and (parts[1].replace('.', '', 1).isdigit() or parts[1].isdigit()):
                player_info = parts[0]
                value = parts[1]
            else:
                player_info = rest
                value = ''

            data.append({
                'Year': 1902,
                'Statistic': stat,
                'PlayerInfo': player_info,
                'Value': value
            })

    return pd.DataFrame(data)

def scrape_1903():
    url = 'https://www.baseball-almanac.com/yearly/yr1903a.shtml'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')
    if not tables:
        raise ValueError("No tables found on the 1903 page")

    table = tables[0]
    rows = table.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            stat = cols[0].get_text(strip=True)
            if stat.lower() == 'statistic':
                continue
            data.append({
                'Year': 1903,
                'Statistic': stat,
                'Name(s)': cols[1].get_text(strip=True),
                'Team(s)': cols[2].get_text(strip=True),
                'Value': cols[3].get_text(strip=True)
            })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df_1902 = scrape_1902()
    df_1903 = scrape_1903()

    combined_df = pd.concat([df_1902, df_1903], ignore_index=True)
    combined_df.to_csv('mlb_1902_1903_comparison.csv', index=False)

    print("1902 data sample:")
    print(df_1902.head(10))
    print("\n1903 data sample:")
    print(df_1903.head(10))
    print("\nCombined data sample:")
    print(combined_df.head(20))
