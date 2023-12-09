import csv
from datetime import datetime


now = datetime.now()
formatted_date = now.strftime("%Y.%m.%d %H_%M_%S")
path_to_file = f'result_dir/{formatted_date}.csv'


def write_first_row_csv():

    with open(path_to_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Ссылка на продукт',
                'Наименование',
                'Цена',
                'Рейтинг пользователей',
                'Описание продукта',
                'Инструкция по применению',
                'Cтрана-производитель'
            )
        )


def write_data_csv(row):

    with open(path_to_file, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(row)
