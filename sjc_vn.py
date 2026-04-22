from bs4 import BeautifulSoup
import requests
import csv
from datetime import date, timedelta

def get_gold_prices(target_date):
    # Định dạng ngày theo yêu cầu của URL (dd-mm-yyyy)
    date_str = target_date.strftime('%d-%m-%Y')
    url = f'https://webgia.com/gia-vang/sjc/{date_str}.html'

    try:
        source = requests.get(url, timeout=10).text
        article = BeautifulSoup(source, 'lxml')
        table = article.find('table')
        rows = []

        if not table:
            rows.append(None)

        for row in table.tbody.find_all('tr'):
            cols = row.find_all('td')
            if cols:
                data = [col.get_text(strip=True) for col in cols]
                rows.append(data)
        # return rows[-2]
        date = rows[-1][0].split(' ')[-1]   # Lấy ngày tại thời điểm đóng giao dịch, định dạng dd-mm-yyyy
        buy = rows[-2][2].split(' ')[0]     # Lấy giá mua tại thời điểm đóng giao dịch
        sell = rows[-2][3].split(' ')[0]    # Lấy giá bán tại thời điểm đóng giao dịch

        return date, buy, sell
    except Exception as e:
        return None

# Cấu hình khoảng thời gian cần lấy dữ liệu
start_date = date(2020, 1, 1)
end_date = date(2026, 4, 21)

all_data = []
current = start_date

while current <= end_date:
    row = get_gold_prices(current)
    if row:
        all_data.append(row)
    current += timedelta(days=1)

# Lưu file .csv
with open('sjc_vn.csv', 'w', newline='', encoding='utf-8-sig') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['Date', 'Buy Price', 'Sell Price'])    # Ghi tiêu đề headers
    csv_writer.writerows(all_data)                              # Ghi dữ liệu vào file .csv
