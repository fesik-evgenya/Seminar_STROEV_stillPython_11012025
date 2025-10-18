# 1. Скрапинг
# requests + Ds4

# подключение библиотек
import requests
from bs4 import BeautifulSoup
import re
import time


# time.sleep(10) - прерывает каждый запрос на 10 секунд
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

# сбор данных по API (Работа России)
# подключение библиотек
# import  requests

# задание запроса
region_code = '57'
offset = 0

#1
# url_api = f'http://opendata.trudvsem.ru/api/v1/vacancies/region/{region_code}?offset={offset}&limit=100'

#2
url_api = 'http://opendata.trudvsem.ru/api/v1/vacancies'
params = {
    'region_code': '57',
    'offset': 0
}

# отправка запроса
#1
# answer = requests.get(url_api)

#2
answer = requests.get(url_api, params=params)

# анализ ответа сервера
# код завершения операции
print(answer.status_code)

# содержимое ответа
print(answer.text)

# ответ сервера получен в формате JSON в виде строки
# для удобства работы необходимо преобразовать строку в словарь
# 1) у объекта response есть метод .json()
# 2) в пакете json есть метод loads() для загрузки содержимого словаря из строки
# 3) Pandas -> .explode() & .json_normalize()

# преобразование str в dict
import  json

#1
# ans_json = answer.json()

#2
ans_json = json.loads(answer.text) # встроенный метод

# разбор полученного словаря
# .keys(), .values(), .items()
# так как это ans_json словарь, необходимо исследовать по ключам

# просмотр всех ключей
ans_json.keys()

# ключ 'status'
ans_json.get('status', 'ERROR')

# ключ 'request'
ans_json.get('request', 'ERROR')

# ключ 'meta'
ans_json.get('meta', 'ERROR')

# ключ 'meta'
ans_json.get('meta', 'ERROR')

# ключ 'results'
ans_json.get('results', 'ERROR')

# видим, что здесь находятся все найденные результатыб
# определим тип этой структуры
print(type(ans_json.get('results'))) # это словарь
# просмотр ключей словаря
ans_json.get('results').keys()
# ключ 'vacancies'
ans_json.get('results').get('vacancies')

# видим, что это полученная структура список - возможно, вакансии
lst_vacancies = ans_json.get('results').get('vacancies')

# разбор отдельной вакансии
print(lst_vacancies[0])

# проверка типа
print(type(lst_vacancies[0]))

# просмотр ключей
print(lst_vacancies[0].keys())

# собираемые поля
## 'region_name', 'name', 'inn', 'creation_date', 'salary_min', 'job_name',
## 'duty'
lst_keys = ['region_name', 'name', 'inn', 'creation_date',
            'salary_min', 'job_name', 'duty' ]
dct_vac = dict.fromkeys(lst_keys, None)

for vac in dct_vac:
    dct_vac['region_name'] = vac['vacancy']['region']['name']
    dct_vac['company_name'] = vac.get('vacancy').get('region').get('company_name')
    dct_vac['inn'] = vac.get('vacancy').get('region').get('inn')
    dct_vac['salary_min'] = vac.get('vacancy').get('region').get('creation_date')
    dct_vac['creation_date'] = vac.get('vacancy').get('region').get('salary_min')

# о товаре
item_about = soup_item_page.select_one('section[data-testid="descriptionBlock"]').get_text(strip=True)
