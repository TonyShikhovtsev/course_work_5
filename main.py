from src.api import HeadHunterAPIVacancies, HeadHunterAPIEmployers
from src.db_functions import create_database, database_parameters, process_to_db_employers, process_to_db_vacancies
from src.manager import DBManager



def main():
    """
    Основная функция с выводом информации в консоль (в том числе средняя ЗП и вывод вакансий с
    ЗП выше средней
    """
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
    vacancies_search = database.get_vacancies_with_keyword('Руководитель')


    print(f"Список с компаниями: {companies}")
    print(f"Список с вакансиями: {vacancies}")
    print(f"Средняя зарплата: {avg_salary}")
    print(f"Список вакансий с з/п выше средней: {vacancies_higher_avg}")
    print(f"Список вакансий по ключевому слову: {vacancies_search}")

if __name__ == "__main__":
    main()

