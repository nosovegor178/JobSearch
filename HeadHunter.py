import requests
from general_functions import gets_the_arithmetic_mean, predict_salary
from itertools import count
from urllib.error import HTTPError


def take_page_payload(page, text_for_searching):
    city_of_vacancie = 1
    url = "https://api.hh.ru/vacancies"
    headers = {"HH-User-Agent": ""}
    payload = {"text": text_for_searching,
               "area": city_of_vacancie,
               "per_page": 100,
               "page": page
    }
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()
    page_payload = response.json()
    return page_payload


def take_all_pages(programming_language):
    hh_jobs = []
    text_for_searching = "Программист {}".format(programming_language)
    page_payload = take_page_payload(0, text_for_searching)
    number_of_pages = page_payload['pages']
    for page_number in range(0, number_of_pages):
        try:
            page_payload = take_page_payload(page_number, text_for_searching)
            hh_jobs.append(page_payload)
        except HTTPError as error:
            if error.code == 403:
                
            else:
                raise
    print(len(hh_jobs))
    return hh_jobs


def predict_rub_salary(job_salary):
    vacancie_salary = job_salary
    if job_salary is None:
        job_currency = {'from': 0,
                        'to': 0,
                        'currency': 'RUR',
                        'gross': False
        }
        mid_rub_salary = predict_rub_salary(job_currency)
    else:
        vacancie_currency = job_salary['currency']
        if vacancie_currency == 'RUR':
            mid_rub_salary = predict_salary(vacancie_salary['from'],
                                                    vacancie_salary['to'])
            return mid_rub_salary


def take_mid_salaries(job_vacancies):
    mid_salaries = []
    for job_vacancy in job_vacancies:
        mid_salary = predict_rub_salary(job_vacancy['salary'])
        mid_salaries.append(mid_salary)
    return mid_salaries


def create_languages_rating_for_hh(programming_languages):
    languages_rate = []
    for programming_language in programming_languages:
        hh_jobs = take_all_pages(programming_language)
        all_vacancies = hh_jobs[0]['items']
        number_of_vacancies = hh_jobs[0]['found']
        mid_salaries = take_mid_salaries(all_vacancies)
        average_salary_by_language = gets_the_arithmetic_mean(mid_salaries)
        language_rate = {programming_language: {
            'vacancies_found': number_of_vacancies,
            'vacansies_proceed': len(mid_salaries),
            'average_salary': int(average_salary_by_language)
        }}
        languages_rate.append(language_rate)
    return languages_rate
