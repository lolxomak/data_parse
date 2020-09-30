import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://www.telavivbroker.com'
URL = 'https://www.telavivbroker.com/location/telavivsales/page/'


HEADERS ={
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

def get_html(url, params=''):
      r = requests.get(url, headers=HEADERS, params=params)
      return r

def normalize_string(s):
      symbols = filter(lambda x: ord(x) < 128, s)
      return ''.join(symbols)

def make_number(s):
      symbols = filter(lambda x: (ord(x) < 128) and (x.isdigit()), s)
      return ''.join(symbols)

def get_text_if_possible(item, params):
      it = item.find(params)
      return "" if not it else it.get_text()

def get_content(html):
      soup = BeautifulSoup(html, 'html.parser')
      items = soup.find_all('div', class_='listing', )
      cards = []
      for item in items:
            dct = {
                  'title': item.find('div', class_='wpsight-listing-title'),
                  'link': item.find('div', class_='wpsight-listing-title'),
                  'price': item.find('div', class_='wpsight-listing-price'),
                  'bedrooms': item.find('span', class_='listing-details-value'),
                  'bathrooms': item.find('span', class_='listing-details-2 listing-details-detail'),
                  'living_area': item.find('span', class_='listing-details-4 listing-details-detail')
            }
            if dct['link']:
                  dct['link'] = dct['link'].find('a')
                  if dct['link']:
                        dct['link'] = dct['link'].get('href')
            if dct['bathrooms']:
                  dct['bathrooms'] = dct['bathrooms'].find('span', class_='listing-details-value')
            if dct['living_area']:
                  dct['living_area'] = dct['living_area'].find('span', class_='listing-details-value')
            number_items = {'price', 'bedrooms', 'bathrooms', 'living_area'}
            for k, v in dct.items():
                  if dct[k]:
                        if k == 'title':
                              dct[k] = dct[k].get_text(strip=True)
                        elif k != 'link':
                              dct[k] = dct[k].get_text()
                        if k in number_items:
                              dct[k] = make_number(dct[k])
                        else:
                              dct[k] = normalize_string(dct[k])
            cards.append(dct)
      return cards

def save_to_csv(items, path):
      with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';', )
            writer.writerow(['title', 'link', 'price', 'bed', 'bath', 'area'])
            for item in items:
                  writer.writerow([item['title'], item['link'], item['price'], item['bedrooms'], item['bathrooms'], item['living_area']])


def parser(pages=None):
      if pages is None:
            PAGENATION = input('Укажите количество старниц для парсинга: ')
            PAGENATION = int(PAGENATION.strip())
      else:
            PAGENATION = pages
      html = get_html(F"{URL}/1")
      if html.status_code == 200:
            cards = []
            for page in range(1, PAGENATION+1):
                  print(f'Идет парсинг страницы: {page}')
                  html = get_html(f"{URL}/{page}")
                  cards.extend(get_content(html.text))
                  save_to_csv(cards, CSV)
            pass
      else:
            print('Error')


if __name__ == '__main__':
      parser()