import requests
from general_functions import gets_the_arithmetic_mean, predict_salary


def take_vacancies(api_key, programming_language):
    full_period = 0
    url = 'https://api.superjob.ru/2.2/vacancies'
    headers = {'X-Api-App-Id': api_key}
    payload = {'town': 'Москва',
               'keyword': 'Программист {}'.format(programming_language),
               'period': full_period
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    sj_vacancies = response.json()
    return sj_vacancies


def predict_rub_salary_for_sj(job_vacancy):
    if job_vacancy['currency'] == 'rub':
        mid_rub_salary = predict_salary(job_vacancy['payment_from'],
                                        job_vacancy['payment_to'])
        return mid_rub_salary


def take_mid_salaries(job_vacancies):
    mid_salaries = []
    for job_vacancy in job_vacancies:
        mid_salary = predict_rub_salary_for_sj(job_vacancy)
        mid_salaries.append(mid_salary)
    return mid_salaries


def create_languages_rating_for_sj(programming_languages, api_key):
    languages_rate = []
    for programming_language in programming_languages:
        sj_jobs = take_vacancies(api_key, programming_language)
        mid_salaries = take_mid_salaries(sj_jobs['objects'])
        mid_language_salary = gets_the_arithmetic_mean(mid_salaries)
        language_rate = {programming_language: {
            'vacancies_found': sj_jobs['total'],
            'vacansies_proceed': len(mid_salaries),
            'average_salary': int(mid_language_salary)
        }}
        languages_rate.append(language_rate)
    return languages_rate
