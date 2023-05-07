import requests
from statistics import median


def take_vacancies(programming_language):
    page = 0
    pages_number = 1
    hh_jobs = []
    url = "https://api.hh.ru/vacancies"
    headers = {"HH-User-Agent": ""}
    payload = {
            "text": "Программист {}".format(programming_language),
            "area": 1,
            "period": 30,
            "only_with_salary": "true",
            "page": page
        }
    while page < pages_number:
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        page_payload = response.json()
        pages_number = page_payload['page']
        page += 1
        hh_jobs.append(page_payload)
    return hh_jobs


def predict_rub_salary(vacancies):
    vacancies_salaries = []
    mid_salaries = []
    for vacancie in vacancies[0]['items']:
        salary = vacancie['salary']
        vacancies_salaries.append(salary)
    for vacancie_salary in vacancies_salaries:
        if vacancie_salary['currency'] == 'RUR':
            if vacancie_salary['from'] is None:
                salary = vacancie_salary['to'] * 0.8
                mid_salaries.append(salary)
            elif vacancie_salary['to'] is None:
                salary = vacancie_salary['from'] * 1.2
                mid_salaries.append(salary)
            else:
                salary = [vacancie_salary['from'], vacancie_salary['to']]
                mid_salary = median(salary)
                mid_salaries.append(mid_salary)
        else:
            None
    return mid_salaries


def create_languages_rating(programming_languages):
    languages_rating = {}
    for programming_language in programming_languages:
        hh_jobs = take_vacancies(programming_language)
        mid_salaries = predict_rub_salary(hh_jobs)
        mid_language_salary = median(mid_salaries)
        language_rate = {
            "vacancies_found": hh_jobs[0]['found'],
            "vacansies_proceed": len(mid_salaries),
            "average_salary": int(mid_language_salary)
        }
        languages_rating[programming_language] = language_rate
    return languages_rating


if __name__ == '__main__':
    programming_languages = {
                            "Python",
                            "Java",
                            "JavaScript",
                            "Ruby",
                            "PHP",
                            "C++",
                            "C",
                            "C#",
                            "Go"
                        }
    languages_rating = create_languages_rating(programming_languages)
    print(languages_rating)
