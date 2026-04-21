from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://coreyms.com').text

csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])

soup = BeautifulSoup(source, 'lxml')
# print(soup.prettify())

try:
    article = soup.find('div', class_='container')
    # print(article.prettify())

    headline = article.a.text
    # print(headline)

    summary = article.p.text
    # print(summary)

    link = article.find('a', class_='youtube-link')['href']
    link_id = link.split('/')[-1]
except Exception as e:
    link_id = None

# print(link_id)
print()

csv_writer.writerow([headline, summary, link_id])
csv_file.close()

""" with open('sample.html') as f:
    soup = BeautifulSoup(f, 'lxml')

for article in soup.find_all('div', class_='article'):
    # print(article)

    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary) """
