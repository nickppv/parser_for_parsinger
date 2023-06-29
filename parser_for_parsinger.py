from bs4 import BeautifulSoup
import requests

result = 0
result_dict = {}
url = 'https://parsinger.ru/html/index1_page_1.html'

response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
# находим информацию ссылки на группы товаров
tag_categories = soup.find(
    'div', {'class': 'nav_menu'}).find_all('a'
                                           )
# убираем теги и др символы до создания "правильной" части ссылки на категорию
link_categories = [
    i['href'].rstrip('1.html').rstrip('_page_') for i in tag_categories
    ]

# берем ссылки на группы товаров и проходимся по ним,
# определяем кол-во страниц в категории и вносим ссылки на них в список
for i in link_categories:
    url = f'https://parsinger.ru/html/{i}_page_1.html'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # находим полностью тег с ссылкой
    tag_paginator_link = soup.find('div', {'class': 'pagen'}).find_all('a')
    # убираем теги и лишние символы до создания "правильной" части ссылки
    paginator_link = [i['href'].split('_', 1)[1] for i in tag_paginator_link]

    # переходим по страницам пагинатора и находим информацию о товаре
    for j in paginator_link:
        # создаем ссылку на категорию и страницу
        url_page_link = f'https://parsinger.ru/html/{i}_{j}'
        response = requests.get(url=url_page_link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        # находим полностью тег с ссылкой
        tag_a_goods_links = soup.find_all('a', 'name_item')
        goods_links = [i['href'] for i in tag_a_goods_links]

        # собираем ссылку на каждый товар
        for k in goods_links:
            url_goods = f'https://parsinger.ru/html/{k}'
            response = requests.get(url=url_goods)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            price = int(
                soup.find('span', id='price').text.strip(' руб')
                )
            amount = int(
                soup.find('span', id='in_stock').text.lstrip('В наличии: ')
                )
            result += price * amount
            brand = soup.find('li', id='brand').text.lstrip('"Бренд: ')
            model = soup.find('li', id='model').text.strip('"Модель: ')
            type = soup.find('p', id='p_header').text
            result_dict[f'{brand}, {model}'] = [f'Тип: {type}, Цена: {price}']
for i, k in result_dict.items():
    print(f'{i}: {k}')
print('Стоимость всех товаров на сайте: ', result)
