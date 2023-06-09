from terminaltables import AsciiTable
from dotenv import load_dotenv
from SuperJob import get_vacancies_statistics
from HeadHunter import create_languages_rating_for_hh
import os


def create_table_raitings(language_raiting):
    table_raitings = []
    for language_name, language_rate in language_raiting.items():
        instance_content = [language_name,
                            language_rate['vacancies_found'],
                            language_rate['vacancies_processed'],
                            language_rate['average_salary']
        ]
        language_instance = []
        language_instance.extend(instance_content)
        table_raitings.append(language_instance)
    return table_raitings


def create_table_content(website_raiting):
    table_insides = [
        ['Язык программирования',
         'Вакансий найдено',
         'Вакансий обработанно',
         'Средняя зарплата']
    ]
    for language_raiting in website_raiting:
        table_raitings = create_table_raitings(language_raiting)
        for table_raiting in table_raitings:
            table_insides.append(table_raiting)
    return table_insides


def create_table(website_raiting, website_name):
    title = '{} Moscow'.format(website_name)
    table_insides = create_table_content(website_raiting)
    table_instance = AsciiTable(table_insides, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance


if __name__ == '__main__':
    load_dotenv()
    hh_raiting = []
    sj_raiting = []
    sj_api_key = os.environ['SJ_SECRET_KEY']
    programming_languages = [
            'Python',
            'Java',
            'JavaScript',
            'Ruby',
            'PHP',
            'C++',
            'C',
            'C#',
            'Go'
        ]
    hh_raiting = create_languages_rating_for_hh(programming_languages)
    sj_raiting = get_vacancies_statistics(programming_languages,
                                                sj_api_key)
    websites_raiting = {'HeadHunter': hh_raiting,
                        'SuperJob': sj_raiting
    }
    for website_name, website_raiting in websites_raiting.items():
        table_instance = create_table(website_raiting, website_name)
        print('{}\n'.format(table_instance.table))
