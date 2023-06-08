import requests
from itertools import count
from general_functions import gets_the_arithmetic_mean, predict_salary
from pprint import pprint
import os


def take_vacancies_in_page(api_key, programming_language, page):
    full_period = 0
    url = 'https://api.superjob.ru/2.2/vacancies'
    headers = {'X-Api-App-Id': api_key}
    payload = {
        'town': 'Москва',
        'keyword': 'Программист {}'.format(programming_language),
        'period': full_period,
        'page': page
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    sj_vacancies = response.json()
    return sj_vacancies


def get_vacancies_statistics(programming_languages, api_key):
    averages_salaries = []
    all_pages_salaries = []
    for programming_language in programming_languages:
        for page in count(0):
            page_payload = take_vacancies_in_page(api_key,
                                                  programming_language,
                                                  page)
            for vacancy in page_payload['objects']:
                if not (vacancy['payment_to'] or vacancy['payment_from']):
                    continue
                if not vacancy['currency'] == 'rub':
                    continue
                average_salary = predict_salary(vacancy['payment_from'],
                                                vacancy['payment_to']
                )
                averages_salaries.append(average_salary)
            if not page_payload['more']:
                break
        if averages_salaries:
            arithmetics_mean = gets_the_arithmetic_mean(averages_salaries)
            average_salary = int(arithmetics_mean)
        else:
            average_salary = None
        vacancies_amount = page_payload['total']
        vacancies_statistics = {programming_language: {
            'average_salary': average_salary,
            'vacancies_found': vacancies_amount,
            'vacancies_processed': len(averages_salaries)
        }}
        all_pages_salaries.append(vacancies_statistics)
    return all_pages_salaries
