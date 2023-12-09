import time

from csv_writer import write_first_row_csv
from exceptions import StatusCode403, StatusCodeNot200
from parser import parse_page


def main():

    write_first_row_csv()

    current_page = 1

    while True:
        more_pages = True
        try:
            more_pages = parse_page(current_page)
        except StatusCode403 as er:
            print(f'Вы забанены!: {er}')
            print(f'{er.answer_status_code}')
            print(f'{er.answer_text}')
            exit()
        except StatusCodeNot200 as er:
            print(f'Вы код ответа не 200!: {er}')
            print(f'{er.answer_status_code}')
            print(f'{er.answer_text}')
            input(f'Нажмите Enter, чтоб возобновить работу программы:')
        except Exception as er:
            print(f'Неизвестная ошибка!: {er}')
            print(f'{er.args}')
            input(f'Нажмите Enter, чтоб возобновить работу программы:')

        if not more_pages:
            break
        current_page += 1
        time.sleep(3)

    print(f'Парсинг завершён!')


if __name__ == '__main__':
    main()
