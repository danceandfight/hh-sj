# HeadHunter / SuperJob analysis 

This program searches [headhunter.ru](headhunter.ru) and [superjob.ru](superjob.ru) all vacations for most popular programming languages and shows statistics for the last 30 days (how many vactions, average salary).

### How to install

For using this program you must register on [superjob.ru](superjob.ru) only and get `Secret Key` in your profile. Secret key looks like `secret_key = 'v3.r.130240347.fb88cc3de1ffe83eac1e6de57de06cad5cc2b5ca.24b9f3264593d2ed5e5f8396762dd0a7107a56e1'`. Then create `.env` file in program folder and add secret key there using this form: `SECRET_KEY='v3.r.130240347.fb88cc3de1ffe83eac1e6de57de06cad5cc2b5ca.24b9f3264593d2ed5e5f8396762dd0a7107a56e1`.

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).