from config import config
from src.utils import get_company, get_vacancies, create_database, save_data_to_database
from src.postgres_dbm import DBManager


def main():
    employee_ids = [
        '4194553',
        '753341',
        '41862',
        '2664870',
        '9757724',
        '625332',
        '4112759',
        '205152',
        '52389',
        '3529'
    ]

    params = config()
    company_list = get_company(employee_ids)
    vacancy_list = get_vacancies(employee_ids)
    create_database('hh_company', params)
    save_data_to_database('hh_company', company_list, vacancy_list, params)

    answer = input('В каком виде представить информацию:\n'
                   '1 - список всех компаний и количество вакансий у каждой компании\n'
                   '2 - список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на'
                   ' вакансию\n'
                   '3 - средняя зарплата по вакансиям\n'
                   '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                   '5 - список всех вакансий, в названии которых содержатся переданные в метод слова, например python\n'
                   'Поиск по: ')

    result = DBManager()
    try:
        if answer == '1':
            print(result.get_companies_and_vacancies())
        elif answer == '2':
            print(result.get_all_vacancies())
        elif answer == '3':
            print(result.get_avg_salary())
        elif answer == '4':
            print(result.get_vacancies_with_higher_salary())
        elif answer == '5':
            print(result.get_vacancies_with_keyword('python'))
    except:
        pass


if __name__ == '__main__':
    main()
