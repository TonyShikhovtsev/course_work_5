from src.config import config
import psycopg2


def database_parameters():
    db_params = config()  # Получаем параметры из файла database.ini
    return db_params


def create_database(db_name: str, params: dict):
    connection = psycopg2.connect(dbname='postgres', **params)
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(f'CREATE DATABASE {db_name}')
    except psycopg2.ProgrammingError:
        pass

    cursor.close()
    connection.close()

    with psycopg2.connect(dbname=db_name, **params) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
            company_id INT PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            url TEXT
            );

            CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            vacancy_name VARCHAR(255) NOT NULL,
            vacancy_salary INT,
            company_id INT ,
            url TEXT,
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
            );
            """)


def process_to_db_employers(db_name: str, params: dict, data):
    with psycopg2.connect(dbname=db_name, **params) as connection:
        with connection.cursor() as cursor:
            for company in data:
                cursor.execute(
                    """
                    INSERT INTO companies (company_id, company_name, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (company_id) DO UPDATE SET
                        company_name = EXCLUDED.company_name,
                        url = EXCLUDED.url
                    """,
                    (
                        company.json().get('id'),
                        company.json().get('name'),
                        company.json().get('alternate_url'),
                    )
                )


def process_to_db_vacancies(db_name: str, params: dict, data):
    with psycopg2.connect(dbname=db_name, **params) as connection:
        with connection.cursor() as cursor:
            for vacancy in data:
                cursor.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_salary, company_id, url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO UPDATE SET
                        vacancy_name = EXCLUDED.vacancy_name,
                        vacancy_salary = EXCLUDED.vacancy_salary,
                        company_id = EXCLUDED.company_id,
                        url = EXCLUDED.url
                    """,
                    (
                        vacancy['id'],
                        vacancy['name'],
                        vacancy['salary']['from'] if vacancy['salary']['from'] is not None else vacancy['salary']['to'],
                        vacancy['employer']['id'],
                        vacancy['url'],
                    )
                )