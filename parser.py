import re

import requests
import json

from csv_writer import write_data_csv

products_url = "https://goldapple.ru/front/api/catalog/products"
product_card_url = "https://goldapple.ru/front/api/catalog/product-card"
city_id = "c2deb16a-0330-4f05-821f-1d09c93331e6"  # - Санкт-Петербург

headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/119.0.0.0 Safari/537.36'
    }


def get_products(page=1):

    data = {
        "categoryId": 1000000007,  # категория Парфюмерия
        "cityId": f"{city_id}",
        "cityDistrict": None,
        "pageNumber": page,
        "filters": []
    }

    response = requests.post(url=products_url, headers=headers, data=json.dumps(data))
    return response.json()


def get_product_card(product_id: str):

    data = {
        "itemId": f"{product_id}",
        "cityId": f"{city_id}",
        "cityDistrict": None,
        "customerGroupId": "0"
    }

    response = requests.post(url=product_card_url, headers=headers, data=json.dumps(data))
    return response


def parse_products(response):
    products_info = []

    products_raw = response.get('data', {}).get('products', [])

    if len(products_raw) > 0:
        for product in products_raw:
            product_id = product.get('itemId', '')
            product_url = "https://goldapple.ru" + product.get('url', '/404')
            name = product.get('name', '')
            price = product.get('price', {}).get('actual').get('amount', '')
            rating = product.get("reviews", {}).get("rating", "")
            products_info.append(
                (product_id, product_url, name, price, rating)
            )
    return products_info


def parse_country(text: str) -> str:
    try:
        return re.search(r'<br>(.*?)<br>', text).group(1)
    except:
        return ''


def parse_product_card(response) -> tuple:
    """Парсинг данных из get_product_card()"""
    product_card = response.json().get('data', {})
    product_description = product_card.get('productDescription', [])

    desc = ""
    for i in product_description:
        if i.get('text') == "описание":
            desc = json.dumps(
                {
                    'title': i.get('title', ''),
                    'subtitle': i.get('subtitle', ''),
                    'content': i.get('content', '').strip(),
                    'attributes': i.get('attributes', '')
                }, ensure_ascii=False
            )
            break

    manual = ""
    for i in product_description:
        if i.get('text') == "применение":
            manual = i.get('content')
            break

    country = ""
    for i in product_description:
        if i['text'] == "Дополнительная информация":
            country = parse_country(i.get('content', ''))
            break

    return desc, manual, country


def parse_page(page_number: int) -> bool:
    """
    Парсит страницу товаров и сохраняет результаты в csv
       :return
       True - ещё есть страницы с товарами
       False - больше нет страниц с товарами
    """
    print(f'-' * 33)
    print(f'Страница: {page_number}')

    # write_first_row_csv()

    products_counter = 0

    products_res = get_products(page_number)
    products = parse_products(products_res)
    if len(products) == 0:
        return False

    for product in products:
        product_id, product_info1 = product[0], product[1:]

        product_res = get_product_card(product_id)
        product_info2 = parse_product_card(product_res)
        products_counter += 1

        product_full_info = product_info1 + product_info2
        write_data_csv(product_full_info)

        print(f'{products_counter} - {product_full_info}')

    return True
