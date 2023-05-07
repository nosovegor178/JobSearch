from terminaltables import AsciiTable
from dotenv import load_dotenv
from SuperJob import create_languages_rating_for_sj
from HeadHunter import create_languages_rating_for_hh
import os


def create_table_data(website_raiting):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработанно',
            'Средняя зарплата']
    ]
    for language_name, language_raiting in website_raiting.items():
        language_data = []
        language_data.append(language_name)
        language_data.append(language_raiting['vacancies_found'])
        language_data.append(language_raiting['vacansies_proceed'])
        language_data.append(language_raiting['average_salary'])
        table_data.append(language_data)
    return table_data


if __name__ == '__main__':
    load_dotenv()
    super_job_api = os.environ['SuperJob_API']
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
    hh_raiting = create_languages_rating_for_hh(programming_languages)
    sj_raiting = create_languages_rating_for_sj(
        programming_languages,
        super_job_api)
    websites_raiting = [hh_raiting, sj_raiting]
    website_name = ['HeadHunter', 'SuperJob']
    for website_number, website_raiting in enumerate(websites_raiting):
        title = "{} Moscow".format(website_name[website_number])
        table_data = create_table_data(website_raiting)
        table_instance = AsciiTable(table_data, title)
        table_instance.justify_columns[4] = 'right'
        print(table_instance.table)
        print()
