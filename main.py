import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import csv


#  создадим функцию, которая принимает код города mg_geo_id=13067
def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')  # переменная для сохранения текущей даты и времени #datetime
    # аргумент strftime - это формат времени

    # обьект класса UserAgent
    ua = UserAgent()

    # создадим словарь для заголовков, чтобы хоть как-то идентифицировать наши запросы
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    #в запросах странички в параметре куки mg_geo_id=2398 находится этот код города нам нужен для москвы и екб
    cookies = {
        'mg_geo_id' : f'{city_code}'
    }

    # отправляем запрос на сайт
    response = requests.get(url='https://magnit.ru/promo/',headers=headers, cookies=cookies)

    # # сохраним ответ в html файл
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    #
    # with open('index.html', encoding='utf8') as file:
    #     src = file.read()  # откроем, прочитаем и сохраним
    # закоментируем сохранение и чтение файла и сразу передадим ответ запроса в beatifulsoup

    soup = BeautifulSoup(response.text, 'lxml')

    # находим город
    city = soup.find('a', class_="header__contacts-link header__contacts-link_city").text.strip()

    #собираем все карточки с товарами
    cards = soup.find_all('a', class_="card-sale card-sale_catalogue")

    # в цикле собираем нужную информацию о каждой карточке
    data1 = []
    for card in cards:
        # название продукта
        card_title = card.find('div', class_='card-sale__title').find('p').text.strip()

        # не все товары имеют скидку , есть скидки пенсионерам или скидки на категорию
        #создадим проверку
        try:
            card_sale = card.find('div', class_='card-sale__discount').text.strip()
        except AttributeError:
            continue


        #заберем старую цену
        card_old_price_integer = card.find('div', class_="label__price label__price_old").find('span',class_="label__price-integer").text.strip()
        card_old_price_decimal = card.find('div', class_="label__price label__price_old").find('span',class_="label__price-decimal").text.strip()
        card_old_price = f'{card_old_price_integer}.{card_old_price_decimal}' #старая цена

        # новая цена
        card_new_price_integer = card.find('div', class_="label__price label__price_new").find('span',class_="label__price-integer").text.strip()
        card_new_price_decimal = card.find('div', class_="label__price label__price_new").find('span',class_="label__price-decimal").text.strip()
        card_new_price = f'{card_new_price_integer}.{card_new_price_decimal}' #новая цена

        #дата акции
        date = card.find('div',class_='card-sale__date').text.strip().replace('\n',' ') #тег p имел перенос строки мы заменили на пробел
        data1.append(
            [card_title,card_sale,card_old_price,card_new_price,date]
        )
        # продолжаем записывать в csv файл данные
    with open(f"{city}_{cur_time}.csv", 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')  # создаем писателя
        writer.writerow(
            [
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
                'Время акции',
            ]
        )
        writer.writerows(
            data1
        )
    print(f'кто-то записал файл')
    return f'{city}_{cur_time}.csv'

def main():
    collect_data(city_code='2398')

if __name__ == '__main__':
    main()
