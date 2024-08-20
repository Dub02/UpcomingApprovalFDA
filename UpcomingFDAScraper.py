import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_fda_page(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    fda_grid = soup.find('div', {'class': 'fdaGrid'})
    rows = fda_grid.find_all('div', class_=['gecCalContent', 'gecCalAltContent'])

    data = []
    for row in rows:
        company_div = row.find('div', class_='tblContent1')
        drug_div = row.find('div', class_='tblContent2')
        event_div = row.find('div', class_='tblContent3')
        outcome_div = row.find('div', class_='tblContent4')
        company_name = company_div.get_text(separator=" ", strip=True)
        drug_name = drug_div.get_text(separator=" ", strip=True)
        event_details = event_div.get_text(separator=" ", strip=True)
        outcome_details = outcome_div.get_text(separator=" ", strip=True)
        
        ticker = company_div.find('a').text.strip()
        data.append({
            'Company': company_name,
            'Ticker': ticker,
            'Drug': drug_name,
            'Event Details': event_details,
            'Outcome Details': outcome_details
        })
    return data

urls = [
    "https://www.rttnews.com/corpinfo/fdacalendar.aspx?PageNum=4",
    "https://www.rttnews.com/corpinfo/fdacalendar.aspx?PageNum=3"
]
all_data = []
for url in urls:
    all_data.extend(scrape_fda_page(url))

df = pd.DataFrame(all_data)

print(df)

df.to_csv('combined_rtt_fda_calendar.csv', index=False)
