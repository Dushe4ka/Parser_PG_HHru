from config import config
from utils import get_company, get_vacancies, create_database, save_data_to_database


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
    print(company_list)
    create_database('hh_company', params=params)
    save_data_to_database('hh_company', company_list, vacancy_list, params=params)


if __name__ == '__main__':
    main()
