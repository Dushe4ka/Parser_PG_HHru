import requests
import psycopg2


def get_url(employee_id):
    """Поиск по названию"""
    try:
        params = {
            "per_page": 20,
            "employer_id": employee_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        r = requests.get("https://api.hh.ru/vacancies/", timeout=1, params=params)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error")
        print(errh.args[0])
        # Prints the response code
    return r.json()['items']


def get_company(employee_ids):
    company_list = []
    for employee_id in employee_ids:
        conn_name = []
        conn_url = []
        employee = get_url(employee_id)
        for i in employee:
            conn_name.append(i['employer']['name'])
            conn_url.append(i['employer']['url'])
        unique_company_name = set(conn_name)
        unique_company_url = set(conn_url)
        for company in unique_company_name:
            for url in unique_company_url:
                company_list.append({'companies': {'company_name': company, 'company_url': url}})
    return company_list


def get_vacancies(employee_ids):
    vacancies_list = []
    for employee_id in employee_ids:
        vacancies = get_url(employee_id)
        for vacancy in vacancies:
            if vacancy['salary']['from'] is not None and vacancy['salary']['to'] is not None:
                vacancies_list.append({'vacancies': {'vacancy_name': vacancy['name'],
                                                     'city': vacancy['area']['name'],
                                                     'salary_from': vacancy['salary']['from'],
                                                     'salary_to': vacancy['salary']['to'],
                                                     'publish_date': vacancy['published_at'],
                                                     'vacancy_url': vacancy['alternate_url'],
                                                     'company_name': vacancy['employer']['name']}})
    return vacancies_list


def create_database(database_name, params):
    """Создание базы данных и таблиц для сохранения данных компаниях и их вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name};")
    except:
        pass
    cur.execute(f"CREATE DATABASE {database_name};")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies
            (company_id serial primary key,
            company_name varchar(100) not null,
            url_company text);
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies
            (vacancy_id serial primary key,
            company_id int references companies(company_id),
            vacancy_name varchar(100) not null,
            city_name varchar(100),
            publish_date date,
            company_name varchar(100) not null,
            salary_from int
            salary_to int
            url_vacancy text);
            """)

    conn.commit()
    conn.close()


def save_data_to_database(database_name, data_companies, data_vacancies, **params):
    """Сохранение данных о компаниях и их вакансиях в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for data_company in data_companies:
            company = data_company['companies']
            cur.execute("""
                INSERT INTO companies (company_name, url_company)
                VALUES (%s, %s);
                returning company_id;
                """, (company['company_name'], company['company_url']))
            company_id = cur.fetchone()[0]
            for data_vacancy in data_vacancies:
                vacancy = data_vacancy['vacancies']
                cur.execute("""
                    INSERT INTO vacancies(company_name, company_id, vacancy_name, city_name, publish_date, salary_from,
                    salary_to, url_vacancy)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                            (vacancy['company_name'], company_id, vacancy['vacancy_name'],
                             vacancy['city'], vacancy['publish_date'], vacancy['salary_from'],
                             vacancy['salary_to'], vacancy['vacancy_url'])
                    )

    conn.commit()
    conn.close()