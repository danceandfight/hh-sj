# HeadHunter / SuperJob analysis 

This program searches [headhunter.ru](headhunter.ru) and [superjob.ru](superjob.ru) all vacancies for most popular programming languages and shows statistics for the last 30 days (how many vactions, average salary).

### How to install

For using this program you must register on [superjob.ru](superjob.ru) only and get `Secret Key` in your profile. Secret key looks like `secret_key = 'v3.r.130240347.fb88cc3de1ffe83eac1e6de57de06cad5cc2b5ca.24b9f3264593d2ed5e5f8396762dd0a7107a56e1'`. Then create `.env` file in program folder and add secret key there using this form: `SJ_SECRET_KEY='v3.r.130240347.fb88cc3de1ffe83eac1e6de57de06cad5cc2b5ca.24b9f3264593d2ed5e5f8396762dd0a7107a56e1`.

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

`$ python3 main.py`
```
+HeadHunter Москва------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java                  | 1853             | 435                 | 167329           |
| Python                | 1443             | 342                 | 149902           |
| TypeScript            | 425              | 143                 | 159590           |
| Objective-C           | 167              | 40                  | 174775           |
| GO                    | 384              | 104                 | 173265           |
| Swift                 | 257              | 81                  | 175395           |
| Scala                 | 194              | 38                  | 187039           |
| Ruby                  | 210              | 71                  | 152119           |
| C                     | 357              | 178                 | 132549           |
| C++                   | 172              | 78                  | 133403           |
| JavaScript            | 2623             | 764                 | 134795           |
| PHP                   | 1148             | 575                 | 121743           |
| C#                    | 1090             | 342                 | 147673           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Москва--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java                  | 17               | 8                   | 80206            |
| Python                | 12               | 8                   | 74362            |
| TypeScript            | 1                | 0                   | 0                |
| Objective-C           | 3                | 1                   | 100000           |
| GO                    | 0                | 0                   | 0                |
| Swift                 | 2                | 0                   | 0                |
| Scala                 | 0                | 0                   | 0                |
| Ruby                  | 0                | 0                   | 0                |
| C                     | 16               | 4                   | 54145            |
| C++                   | 23               | 22                  | 55370            |
| JavaScript            | 51               | 24                  | 67281            |
| PHP                   | 44               | 24                  | 70831            |
| C#                    | 22               | 26                  | 91665            |
+-----------------------+------------------+---------------------+------------------+
```
### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).