# 1. Скрапинг
# requests + Ds4

# подключение библиотек
import requests
from bs4 import BeautifulSoup
import re

# ссылка на ресурс, откуда собираем данные
number_page = 1
url_page = f'https://www.detmir.ru/catalog/index/name/nutrition_feeding/?page={number_page}'

# отправка запроса
answer = requests.get(url_page)

# анализ ответа сервера
print(answer.status_code)

# содержимое ответа
content = answer.text

# конкретная часть ответа - поиск фрагмента текста
smes_NAN = answer.text.find('Смесь NAN')

# разметка текста с помощью конструктора BeautifulSoup
soup = BeautifulSoup(content, 'lxml')

# поиск необходимых компонентов (bs4)
# find_all('название тега', словарь параметров и значений тега) -- поиск всех элементов с указанным оформлением
# find('название тега', словарь параметров и значений тега) -- поиск первого элемента с указанным оформлением

lst_items_by_atribute = soup.find_all('section',attrs={'class':'hR hU h_ bt_9'})
lst_items_by_selector = soup.select('section[data-product-id]')

# исследование одного элемента

# название продукции
(
    lst_items_by_selector[0].find('a', attrs={'class':'h_1'})
                            .get_text(strip=True)
)

# адрес страницы товара
url_item_page = lst_items_by_selector[0].find('a').get('href')

# отправка запроса
answer_item_page = requests.get(url_item_page)

# разметка текста ответа
soup_item_page = BeautifulSoup(answer_item_page.text, 'lxml')

## поиск необходимых элементов

# название товара
item_title = soup_item_page.select_one('h1[data-testid]').get_text(strip=True)

# цена товара
item_price = re.findall(r'\d+', soup_item_page.select_one('p[data-testid]').get_text(strip=True))

# о товаре
item_about = soup_item_page.select_one('section[data-testid="descriptionBlock"]').get_text(strip=True)



