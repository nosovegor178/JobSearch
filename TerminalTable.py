from terminaltables import AsciiTable
from dotenv import load_dotenv
from SuperJob import create_languages_rating_for_sj
from HeadHunter import create_languages_rating_for_hh
import os


def create_table_data(website_raiting):
    table_info = [
        ['Язык программирования',
         'Вакансий найдено',
         'Вакансий обработанно',
         'Средняя зарплата']
    ]
    for language_name, language_raiting in website_raiting.items():
        language_info = []
        language_info.append(language_name)
        language_info.append(language_raiting['vacancies_found'])
        language_info.append(language_raiting['vacansies_proceed'])
        language_info.append(language_raiting['average_salary'])
        table_info.append(language_data)
    return table_info


if __name__ == '__main__':
    load_dotenv()
    sj_api_key = os.environ['SUPER_JOB_API']
    programming_languages = {
            'Python',
            'Java',
            'JavaScript',
            'Ruby',
            'PHP',
            'C++',
            'C',
            'C#',
            'Go'
        }
    hh_raiting = create_languages_rating_for_hh(programming_languages)
    sj_raiting = create_languages_rating_for_sj(programming_languages,
                                                sj_api_key)
    websites_raiting = [hh_raiting, sj_raiting]
    for website_raiting in websites_raiting:
        title = '{} Moscow'.format(website_raiting['website_name'])
        table_info = create_table_data(website_raiting)
        table_instance = AsciiTable(table_info, title)
        table_instance.justify_columns[4] = 'right'
        print(table_instance.table)
        print()
