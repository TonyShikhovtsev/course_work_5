import requests

class HeadHunterAPIVacancies:
    """
    Класс для получения информации с сайта hh.ru по вакансиям
    """
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self):
        employer_ids = ['64174',# 2гис
                        '1740',# Яндекс
                        '3529',# Сбербанк
                        '4339952',# Газпром
                        '78638',# Тинькофф
                        '4181',# ВТБ
                        '80',# Альфа-банк
                        '4394',# ОТП Банк
                        '86391999', #skypro
                        ]
        items = []

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
                    for vacancy in vacancies:
                        if vacancy.get('salary').get('currency') == "RUR":
                            items.append(vacancy)
                else:
                    print(f"Ошибка API. Код состояния: {response.status_code}")
                    break
        return items

class HeadHunterAPIEmployers:
    """
    Класс для получения информации с сайта hh.ru по работодателям
    """
    def __init__(self):
        self.url = "https://api.hh.ru/employers/"

    def get_employers(self):
        employer_ids = ['64174',# 2гис
                        '1740',# Яндекс
                        '3529',# Сбербанк
                        '4339952',# Газпром
                        '78638',# Тинькофф
                        '4181',# ВТБ
                        '80',# Альфа-банк
                        '4394',# ОТП Банк
                        '86391999', #skypro
                        ]
        items = []

        for employer_id in employer_ids:
            url = self.url + employer_id
            response = requests.get(url)
            if response.status_code == 200:
                items.append(response)
            else:
                break
        return items
