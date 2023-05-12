import requests


def mean(numbers):
    numbers = [x for x in numbers if x is not None]
    return float(sum(numbers)) / max(len(numbers), 1)


def take_vacancies(programming_language):
    page = 0
    pages_number = 1
    city_of_vacancie = 1
    job_search_period = 30
    hh_jobs = []
    url = 'https://api.hh.ru/vacancies'
    headers = {'HH-User-Agent': ''}
    while page < pages_number:
        payload = {
            'text': 'Программист {}'.format(programming_language),
            'area': city_of_vacancie,
            'period': job_search_period,
            'page': page
        }
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        page_payload = response.json()
        pages_number = page_payload['page']
        page += 1
        hh_jobs.append(page_payload)
    return hh_jobs


def predict_salary_for_hh(salary_from, salary_to):
    if salary_from is None:
        mid_salary_for_hh = salary_to * 0.8
    elif salary_to is None:
        mid_salary_for_hh = salary_from * 1.2
    else:
        salary = [salary_from, salary_to]
        mid_salary_for_hh = mean(salary)
    return mid_salary_for_hh


def predict_rub_salary(job_salaries):
    vacancie_currency = job_salaries['currency']
    vacancie_salary = job_salaries
    if vacancie_currency == 'RUR':
        mid_rub_salary = predict_salary_for_hh(vacancie_salary['from'],
                                                vacancie_salary['to'])
        return mid_rub_salary


def vacancy_check(job_salary):
    if job_salary is None:
        job_currency = {'from': 0,
        'to': 0,
        'currency': 'RUR',
        'gross': False
        }
        checked_salary = predict_rub_salary(job_currency)
    else:
        checked_salary = predict_rub_salary(job_salary)
    return checked_salary


def take_mid_salaries(job_vacancies):
    mid_salaries = []
    for job_vacancy in job_vacancies:
        mid_salary = vacancy_check(job_vacancy['salary'])
        mid_salaries.append(mid_salary)
    return mid_salaries


def create_languages_rating_for_hh(programming_languages):
    languages_rate = []
    for programming_language in programming_languages:
        hh_jobs = take_vacancies(programming_language)
        all_vacancies = hh_jobs[0]['items']
        number_of_vacancies = hh_jobs[0]['found']
        mid_salaries = take_mid_salaries(all_vacancies)
        average_salary_by_language = mean(mid_salaries)
        language_rate = {programming_language: {
            'vacancies_found': number_of_vacancies,
            'vacansies_proceed': len(mid_salaries),
            'average_salary': int(average_salary_by_language)
        }}
        languages_rate.append(language_rate)
    return languages_rate
