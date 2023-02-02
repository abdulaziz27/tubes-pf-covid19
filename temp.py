'''from flask import Flask, render_template, url_for, request
import requests, json
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

import requests

url = "https://covid-193.p.rapidapi.com/"

headers = {
    "X-RapidAPI-Key": "2d465aec8dmsh34a23d8b9a4a2bfp1b5329jsna409adccd2b3",
    "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

# countries = requests.request("GET", url + 'countries/', headers=headers)
country_search = requests.request("GET", url + 'countries/?search=china', headers=headers)
#c_search = country_search.json()['response'][0]

#statistics = requests.request("GET", url + 'statistics', headers=headers)
#statistics_country = requests.request("GET", url + 'statistics?country=indonesia', headers=headers)
#statistics_all = requests.request("GET", url + 'statistics?country=all', headers=headers)
history_c = requests.request("GET", url + 'history?country=indonesia', headers=headers)

data_stats = statistics.json()
data_stats_c = statistics_country.json()
data_stats_all = statistics_all.json()

print(statistics.json()['results'])

print('*********************')
stats_list = []
for item in data_stats['response']:
    stats = {
        'continent': item['continent'],
        'country': item['country'],
        #'new_case': item['cases']['new'],
        'active': item['cases']['active'],
        'recovered': item['cases']['recovered'],
        'total_case': item['cases']['total'],
        #'new_death': item['deaths']['new'],
        'total_death': item['deaths']['total']
    }
    stats_list.append(stats)
print(stats_list)

stats_list_total_case = sorted(stats_list, key=lambda d: d['total_case'], reverse=True)

#print(stats_list_total_case)


print('*********************')


@app.route("/search", methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        new_list = list(filter(lambda x: (x['country'] == search), stats_list))
        return render_template('navbar.html', search_data = new_list, title = 'Search Data')
    else:
        search.request.args.get['search']


@app.route("/")
def home():

    '''
    def parse_stats(statistics):
        stats_list = []
        for item in statistics['response']:
            stats = {
                'continent': item['continent'],
                'country': item['country'],
                'new_case': item['cases']['new'],
                'active': item['cases']['active'],
                'recovered': item['cases']['recovered'],
                'total_case': item['cases']['total'],
                'new_death': item['deaths']['new'],
                'total_death': item['deaths']['total']
            }
            stats_list.append(stats)
        return stats_list

    #print(sorted(parse_stats(data_stats), key=lambda student: student[2], reverse=True))
    
    t = parse_stats(data_stats)
    '''


    def get_pagination(offset=0, per_page=10):
        return stats_list[offset: offset+per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(stats_list)
    pagination_data = get_pagination(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


    def parse_stats_co(statistics_country):
        stats_co_list = []
        for item in statistics_country['response']:
            stats_c = {
                'country': item['country'],
                'new_case': item['cases']['new'],
                'active': item['cases']['active'],
                'recovered': item['cases']['recovered'],
                'total_case': item['cases']['total'],
                'new_death': item['deaths']['new'],
                'total_death': item['deaths']['total']
            }
            stats_co_list.append(stats_c)
        return stats_co_list
    
    def parse_stats_all(statistics_all):
        stats_all_list = []
        for item in statistics_all['response']:
            stats_all = {
                'new_case': item['cases']['new'],
                'active': item['cases']['active'],
                'recovered': item['cases']['recovered'],
                'total_case': item['cases']['total'],
                'new_death': item['deaths']['new'],
                'total_death': item['deaths']['total']
            }
            stats_all_list.append(stats_all)
        return stats_all_list

    #print(parse_stats_all(data_stats_all))
    return render_template('layout.html', title = "Home", country_stats = parse_stats_co(data_stats_c), statistics = stats_list, all_stats = parse_stats_all(data_stats_all), pagination_data=pagination_data,page=page,per_page=per_page,pagination=pagination)

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title = "Statistics")

@app.route("/infection-risk")
def infection_risk():
    return render_template('infection_risk.html', title = "Infection Risk")

@app.route("/recovery-presentage")
def infection_risk():
    return render_template('recovery_presentage.html', title = "Recovery Presentage")

@app.route("/cfr")
def infection_risk():
    return render_template('cfr.html', title = "CFR")
'''

"""
flask --app app --debug run
"""