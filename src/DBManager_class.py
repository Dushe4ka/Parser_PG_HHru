import psycopg2
from config import config

class DBManager:
    def __init__(self):
        self.db_name = 'hh_companies'

    def execute(self, query):
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
        conn.close()
        return results


    def get_companies_and_vacancies(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        result = self.execute(f'select companies.company_id, vacancies.company_name, '
                              f'count(company_name) as "Кол-во вакансий" '
                              f'from companies join vacancies '
                              f'using(company_name) '
                              f'group by companies.company_id, vacancies.company_name '
                              f'order by company_id')
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
                вакансию."""

        result = self.execute(f'select vacancy_name, company_name, salary_from, salary_to, url_vacancy '
                              f'from vacancies')

        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""

        result = self.execute(f'SELECT AVG(salary_from) AS "Средняя зарплата ОТ", '
                              f'AVG(salary_to) AS "Средняя зарплата ДО" FROM vacancies')
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        result = self.execute(f'select * from vacancies '
                              f'where salary_from >(select avg(salary_from) from vacancies)'
                              f'and salary_to >(select avg(salary_to) from vacancies)'
                              f'order by vacancy_id')
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        result = self.execute(f'select * from vacancies'
                              f'where vacancy_name like "%%s%"', keyword)
        return result


