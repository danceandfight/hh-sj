#!/usr/bin/python3
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

def predict_rub_salary_hh(vacancy):
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

def predict_rub_salary_for_sj(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    return salary_from, salary_to

def table_maker(dict_with_languages_statistics, site):
    title = '{} Москва'.format(site)
    TABLE_HEADER = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    TABLE_DATA = [TABLE_HEADER]
    
    for lang in dict_with_languages_statistics:
        TABLE_ROW = [lang, dict_with_languages_statistics[lang]['vacancies_found'], dict_with_languages_statistics[lang]['vacancies_processed'], dict_with_languages_statistics[lang]['average_salary']]
        TABLE_DATA.append(TABLE_ROW)
    table = AsciiTable(TABLE_DATA, title)
    return table.table

def main():
    url = 'https://api.hh.ru/vacancies'
    list_of_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'GO', 'Objective-C', 'Scala', 'Swift', 'TypeScript']
    headhunter_statistics = {}

    for language in list_of_languages:
        language_vacancies_info = {}
        total_language_vacancies = []
        page = 0
        total_pages = 1
        while page < total_pages:
            payload = {'text': 'Программист Москва {}'.format(language), 'period': '30', 'page': page}
            response = requests.get(url, params=payload)
            total_pages = response.json()['pages']
            total_language_vacancies += response.json()['items']
            vacancies_found = response.json()['found']
            page += 1
        vacancies_processed = 0
        total_salary = 0
        for vacancy in total_language_vacancies:
            salary_from, salary_to = predict_rub_salary_hh(vacancy)
            salary = predict_rub_salary(salary_from, salary_to)
            if salary != None:
                vacancies_processed += 1
                total_salary += salary
        language_vacancies_info['vacancies_found'] = vacancies_found
        language_vacancies_info['vacancies_processed'] = vacancies_processed
        language_vacancies_info['average_salary'] = int(total_salary / vacancies_processed)
        headhunter_statistics[language] = language_vacancies_info
        
    secret_key = os.getenv('SECRET_KEY')
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}

    superjob_statistics = {}
    for language in list_of_languages:
        payload = {'town': 4, 'catalogues': 48, 'keyword': language}
        page = 0
        total_pages = 1
        total_language_vacancies = []
        language_vacancies_info = {}
        while page < total_pages:
            response = requests.get(url, params=payload, headers=headers)
            total_pages = math.ceil(response.json()['total'] / 20)
            page += 1
            total_language_vacancies += response.json()['objects']
        vacancies_processed = 0
        total_salary = 0
        for vacancy in total_language_vacancies:
            salary_from, salary_to = predict_rub_salary_for_sj(vacancy)
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

    print(table_maker(headhunter_statistics, 'HeadHunter'))
    print(table_maker(superjob_statistics, 'SuperJob'))

if __name__ == '__main__':
    load_dotenv()
    main()