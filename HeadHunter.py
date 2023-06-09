import requests
from general_functions import gets_the_arithmetic_mean, predict_salary
from itertools import count


def take_vacancies_in_page(programming_language, page):
    city_of_vacancie = 1
    vacancies_per_page = 100
    text_for_searching = 'Программист {}'.format(programming_language)
    url = 'https://api.hh.ru/vacancies'
    headers = {'HH-User-Agent': ''}
    payload = {
        'text': text_for_searching,
        'area': city_of_vacancie,
        'page': page,
        'per_page': vacancies_per_page
    }
    page_response = requests.get(url, params=payload, headers=headers)
    page_response.raise_for_status()
    return page_response


def take_all_pages_vacancies(programming_language):
    hh_jobs = []
    maximum_number_of_pages = 18
    for page in count(0):
        response = take_vacancies_in_page(programming_language, page)
        page_payload = response.json()
        hh_jobs.append(page_payload)
        if page-1 >= page_payload['page'] or page > maximum_number_of_pages:
            break
    return hh_jobs


def predict_rub_salary(job_salaries):
    vacancie_currency = job_salaries['currency']
    vacancie_salary = job_salaries
    if vacancie_currency == 'RUR':
        mid_rub_salary = predict_salary(vacancie_salary['from'],
                                        vacancie_salary['to'])
        return mid_rub_salary


def vacancy_check(job_salary):
    if not job_salary:
        return 0
    else:
        checked_salary = predict_rub_salary(job_salary)
        return checked_salary


def take_mid_salaries(all_pages):
    mid_salaries = []
    for page in all_pages:
        vacancies_in_page = page['items']
        for job_vacancy in vacancies_in_page:
            mid_salary = vacancy_check(job_vacancy['salary'])
            mid_salaries.append(mid_salary)
    return mid_salaries


def create_languages_rating_for_hh(programming_languages):
    languages_rate = []
    for programming_language in programming_languages:
        all_vacancies = take_all_pages_vacancies(programming_language)
        number_of_vacancies = all_vacancies[0]['found']
        mid_salaries = take_mid_salaries(all_vacancies)
        average_salary_by_language = gets_the_arithmetic_mean(mid_salaries)
        language_rate = {programming_language: {
            'vacancies_found': number_of_vacancies,
            'vacancies_processed': len(mid_salaries),
            'average_salary': int(average_salary_by_language)
        }}
        languages_rate.append(language_rate)
    return languages_rate
