import psycopg2


class DBManager:
    """
    Класс подключения к БД PostgreSQL
    """
    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        results = []
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT c.company_id, c.company_name, COUNT(*) AS vacancy_count
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                GROUP BY c.company_id, c.company_name
                ORDER BY vacancy_count DESC;
                """)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(row)
        return results

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        results = []
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT c.company_name, v.vacancy_name, v.vacancy_salary, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id;
                """)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(row)
        return results

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT AVG(vacancy_salary) FROM vacancies;
                """)
                rows = cursor.fetchall()
                avg_salary = rows[0][0]
        if avg_salary is not None:
            return round(avg_salary, 3)
        else:
            return 0.0  # Возвращаем 0.0, если средняя зарплата не определена.

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        results = []
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT vacancy_id, vacancy_name, vacancy_salary
                FROM vacancies
                WHERE vacancy_salary > (
                  SELECT AVG(vacancy_salary) AS avg_salary
                  FROM vacancies
                );
                """)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(row)
        return results

    def get_vacancies_with_keyword(self, keyword):
        """
        get_vacancies_with_keyword()получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        results = []
        with psycopg2.connect(dbname=self.db_name, **self.params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                        SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')
                        """)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(row)
        return results