from api_hh import HeadHunterAPI
import requests


def main():
    a = ['https://hh.ru/employer/4194553',
         'https://hh.ru/employer/753341?hhtmFrom=vacancy_search_list',
         'https://hh.ru/employer/41862?hhtmFrom=vacancy_search_list',
         'https://hh.ru/employer/2664870?hhtmFrom=vacancy_search_list']
    # response = requests.get(f'https://hh.ru/employer/753341?hhtmFrom=vacancy_search_list')
    # print(response.status_code)
    for i in a:
        print(i)
        response = requests.get(f'{i}')
        print(response.status_code)


if __name__ == '__main__':
    main()
