from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

url = "https://www.baseball-almanac.com/yearly/yr1902a.shtml"

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)
time.sleep(3)

# Extract year
year = url.split("/")[-1].split(".")[0][2:6]

# Extract event title
title = driver.find_element(By.TAG_NAME, "h1").text

# Extract all tables
tables = driver.find_elements(By.TAG_NAME, 'table')

records = []

for table in tables:
    try:
        caption = table.find_element(By.TAG_NAME, 'caption').text
    except:
        caption = "No Caption"

    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if not cells:
            continue  
        data = [cell.text for cell in cells]
        record = {
            "Year": year,
            "Event": title,
            "Table": caption,
            "RowData": data
        }
        records.append(record)

driver.quit()

# Clean and structure the data
structured_records = []

for rec in records:
    row = rec["RowData"]
    if len(row) == 3:
        name, team, value = row
    elif len(row) == 2:
        name, value = row
        team = ""
    else:
        continue  

    structured_records.append({
        "Year": rec["Year"],
        "Event": rec["Event"],
        "Table": rec["Table"],
        "Name": name,
        "Team": team,
        "Value": value
    })


# # Save data
# df = pd.DataFrame(records)
# df.to_csv("mlb_history_1902.csv", index=False)
# print(f"Saved {len(df)} records")

df = pd.DataFrame(structured_records)
df.to_csv("mlb_history_1902_cleaned.csv", index=False)
print(f"Saved {len(df)} cleaned records")


