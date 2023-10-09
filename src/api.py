import requests

class HeadHunterAPIVacancies:
    """Класс для получения информации с сайта hh.ru"""
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self):
        """Получает вакансии с сайта hh.ru без использования токена"""
        employer_ids = ['64174',
                        '1740',
                        '3529',
                        ]
        items = []
        # Получение информации с 5 страниц по 10 результатов на странице
        for employer_id in employer_ids:
            for i in range(5):
                response = requests.get(self.url,
                                        params={
                                            'employer_id': employer_id,
                                            'per_page': 10,
                                            'page': i,
                                            'only_with_salary': True
                                        })
                if response.status_code == 200:
                    vacancies = response.json().get('items', [])
                    # Получение вакансий только с валютой равной Рублю
                    for vacancy in vacancies:
                        if vacancy.get('salary').get('currency') == "RUR":
                            items.append(vacancy)
                else:
                    print(f"Ошибка API. Код состояния: {response.status_code}")
                    break
        return items

class HeadHunterAPIEmployers:
    """Класс для получения информации с сайта hh.ru"""
    def __init__(self):
        self.url = "https://api.hh.ru/employers/"

    def get_employers(self):
        """Получает вакансии с сайта hh.ru без использования токена"""
        employer_ids = ['64174',
                        '1740',
                        '3529',
                        ]
        items = []
        # Получение информации с 5 страниц по 10 результатов на странице
        for employer_id in employer_ids:
            url = self.url + employer_id
            response = requests.get(url)
            if response.status_code == 200:
                items.append(response)
            else:
                break
        return items
