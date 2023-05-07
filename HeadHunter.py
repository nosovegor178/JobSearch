import requests


def mean(numbers):
    numbers = [x for x in numbers if x is not None]
    return float(sum(numbers)) / max(len(numbers), 1)


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


def predict_salary(salary_from, salary_to):
    if salary_from is None:
        mid_salary = salary_to * 0.8
    elif salary_to is None:
        mid_salary = salary_from * 1.2
    else:
        salary = [salary_from, salary_to]
        mid_salary = mean(salary)
    return mid_salary


def predict_rub_salary(vacancie):
    vacancie_salary = vacancie['salary']
    if vacancie_salary['currency'] == 'RUR':
        mid_rub_salary = predict_salary(
            vacancie_salary['from'],
            vacancie_salary['to'])
        return mid_rub_salary
    else:
        None


def take_mid_salaries(vacancies):
    mid_salaries = []
    for vacancie in vacancies:
        mid_salary = predict_rub_salary(vacancie)
        mid_salaries.append(mid_salary)
    return mid_salaries


def create_languages_rating_for_hh(programming_languages):
    languages_rating = {}
    for programming_language in programming_languages:
        hh_jobs = take_vacancies(programming_language)
        mid_salaries = take_mid_salaries(hh_jobs[0]['items'])
        mid_language_salary = mean(mid_salaries)
        language_rate = {
            "vacancies_found": hh_jobs[0]['found'],
            "vacansies_proceed": len(mid_salaries),
            "average_salary": int(mid_language_salary)
        }
        languages_rating[programming_language] = language_rate
    return languages_rating
