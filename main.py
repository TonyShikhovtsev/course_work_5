from src.api import HeadHunterAPIVacancies, HeadHunterAPIEmployers
from src.db_functions import create_database, database_parameters, process_to_db_employers, process_to_db_vacancies
from src.manager import DBManager


def main():
    hh_employers_api = HeadHunterAPIEmployers()
    hh_employers = hh_employers_api.get_employers()
    hh_vacancies_api = HeadHunterAPIVacancies()
    hh_vacancies = hh_vacancies_api.get_vacancies()

    params = database_parameters()
    create_database('hh_vacancies', params)

    process_to_db_employers('hh_vacancies', params, hh_employers)
    process_to_db_vacancies('hh_vacancies', params, hh_vacancies)

    database = DBManager('hh_vacancies', params)
    companies = database.get_companies_and_vacancies_count()
    vacancies = database.get_all_vacancies()
    avg_salary = database.get_avg_salary()
    vacancies_higher_avg = database.get_vacancies_with_higher_salary()


    print(f"Список с компаниями: {companies}")
    print(f"Список с вакансиями: {vacancies}")
    print(f"Средняя зарплата: {avg_salary}")
    print(f"Список вакансий с з/п выше средней: {vacancies_higher_avg}")


if __name__ == "__main__":
    main()

