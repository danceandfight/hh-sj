import os
import requests
import math
from terminaltables import AsciiTable
from dotenv import load_dotenv

def predict_rub_salary(salary_from, salary_to):
    if salary_from != None and salary_to != None:
        return (salary_from + salary_to)/2
    if salary_from != None and salary_to == None:
        return salary_from * 1.2
    if salary_from == None and salary_to != None:
        return salary_to * 0.8

def fetch_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if salary is None:
        salary_from, salary_to = None, None
        return salary_from, salary_to
    if salary['currency'] != 'RUR':
        salary_from, salary_to = None, None
        return salary_from, salary_to
    if salary['from'] != None:
        salary_from = salary['from']
    else: salary_from = None
    if salary['to'] != None:
        salary_to = salary['to']
    else: salary_to = None
    return salary_from, salary_to

def make_table(dict_with_languages_statistics, site):
    title = '{} Москва'.format(site)
    table_header = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_data = [table_header]
    for lang in dict_with_languages_statistics:
        lang_statistics = dict_with_languages_statistics[lang]
        table_row = [lang, lang_statistics['vacancies_found'], lang_statistics['vacancies_processed'], lang_statistics['average_salary']]
        table_data.append(table_row)
    table = AsciiTable(table_data, title)
    return table.table

def get_hh_statistics(list_of_languages):
    url = 'https://api.hh.ru/vacancies'
    headhunter_statistics = {}
    for language in list_of_languages:
        language_vacancies_info = {}
        total_language_vacancies = []
        page = 0
        total_pages = 1
        while page < total_pages:
            payload = {'text': 'Программист Москва {}'.format(language), 'period': '30', 'page': page}
            response = requests.get(url, params=payload)
            if not response.ok or 'error' in response:
                raise requests.exceptions.HTTPError(response['error'])
            else:
                total_pages = response.json()['pages']
                total_language_vacancies += response.json()['items']
                vacancies_found = response.json()['found']
                page += 1
        vacancies_processed = 0
        total_salary = 0
        for vacancy in total_language_vacancies:
            salary_from, salary_to = fetch_rub_salary_hh(vacancy)
            salary = predict_rub_salary(salary_from, salary_to)
            if salary != None:
                vacancies_processed += 1
                total_salary += salary
        language_vacancies_info['vacancies_found'] = vacancies_found
        language_vacancies_info['vacancies_processed'] = vacancies_processed
        language_vacancies_info['average_salary'] = int(total_salary / vacancies_processed)
        headhunter_statistics[language] = language_vacancies_info
    return headhunter_statistics

def get_sj_statistics(list_of_languages):
    SECRET_KEY = os.getenv('SJ_SECRET_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': SECRET_KEY}
    superjob_statistics = {}
    for language in list_of_languages:
        api_code_moscow = 4
        api_code_it = 48
        payload = {'town': api_code_moscow, 'catalogues': api_code_it, 'keyword': language}
        page = 0
        total_pages = 1
        total_language_vacancies = []
        language_vacancies_info = {}
        while page < total_pages:
            response = requests.get(url, params=payload, headers=headers)
            if not response.ok or 'error' in response:
                raise requests.exceptions.HTTPError(response['error'])
            else:
                vacancies_per_page = 20
                total_pages = math.ceil(response.json()['total'] / vacancies_per_page)
                page += 1
                total_language_vacancies += response.json()['objects']
        vacancies_processed = 0
        total_salary = 0
        for vacancy in total_language_vacancies:
            salary_from, salary_to = vacancy['payment_from'], vacancy['payment_to']
            salary = predict_rub_salary(salary_from, salary_to)
            if salary_from or salary_to != 0:
                vacancies_processed += 1
            total_salary += salary
        language_vacancies_info['vacancies_found'] = response.json()['total']
        language_vacancies_info['vacancies_processed'] = vacancies_processed
        if vacancies_processed != 0: 
            language_vacancies_info['average_salary'] = int(total_salary / vacancies_processed)
        else: language_vacancies_info['average_salary'] = 0
        superjob_statistics[language] = language_vacancies_info
    return superjob_statistics

def main():
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'GO', 'Objective-C', 'Scala', 'Swift', 'TypeScript']
    hh_statistics = get_hh_statistics(languages)
    sj_statistics = get_sj_statistics(languages)
    print(make_table(hh_statistics, 'HeadHunter'))
    print(make_table(sj_statistics, 'SuperJob'))

if __name__ == '__main__':
    load_dotenv()
    main()

