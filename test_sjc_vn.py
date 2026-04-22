from bs4 import BeautifulSoup
import requests
import csv

def get_price():
    try:
        url = requests.get('https://webgia.com/gia-vang/sjc/02-01-2020.html').text
        soup = BeautifulSoup(url, 'lxml')
        table = soup.find('table')

        if not table:
            return None
        else:
            rows = []
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if cols:
                    rows.append([col.get_text(strip=True) for col in cols])

        date = rows[-1][0].split(' ')[-1]
        buy = rows[-2][2].split(' ')[0]
        sell = rows[-2][3].split(' ')[0]

        return date, buy, sell
    except Exception as e:
        return None

if __name__ == "__main__":
    get_price()

    with open('test_sjc_vn.csv', 'w') as f:
        row = csv.writer(f)
        row.writerow(['date', 'buy', 'sell'])
        row.writerow(get_price())
