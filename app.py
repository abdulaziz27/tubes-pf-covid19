from flask import Flask, render_template, url_for, request, jsonify
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

import requests


url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"

endpoint_countries = 'countries'
endpoint_world = 'world'

headers = {
	"X-RapidAPI-Key": "45f3db60cemsh852aa24317a3125p1aa9a1jsna01b5be57c21",
	"X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
}

response = requests.request("GET", url + endpoint_countries, headers=headers)
responseWorldData = requests.request("GET", url + endpoint_world, headers=headers)

stats_data = response.json()
world_data = responseWorldData.json()

new_stats_list = []
for item in stats_data:
    stats = {
        'country': item['Country'],
        'total_cases': item['TotalCases'],
        #'new_cases': item['NewCases'],
        'total_deaths': item['TotalDeaths'],
        #'new_death': item['NewDeaths'],
        'total_recovered': item['TotalRecovered'],
        #'new_recovered': item['NewRecovered'],
        'active_cases': item['ActiveCases'],
        'population': item['Population'],
        'cfr': item['Case_Fatality_Rate'],
        'recovery_presentage': item['Recovery_Proporation'],
        'infection_risk': item['Infection_Risk'],

    }
    new_stats_list.append(stats)

sortByCFR = sorted(new_stats_list, key=lambda x: x['cfr'], reverse=True)
sortByRecoveryP = sorted(new_stats_list, key=lambda x: x['recovery_presentage'], reverse=True)
sortByInfectionRisk = sorted(new_stats_list, key=lambda x: x['infection_risk'], reverse=True)

# Menggunakan sorted() untuk mengurutkan data berdasarkan total kematian terendah dan total recovered terbanyak
sorted_data = sorted(new_stats_list, key=lambda x: (x["total_deaths"], x["total_recovered"]), reverse=True)

new_world_data = []
for item in world_data:
    data = {
        'total_cases': item['TotalCases'],
        'new_cases': item['NewCases'],
        'total_deaths': item['TotalDeaths'],
        'new_deaths': item['NewDeaths'],
        'total_recovered': item['TotalRecovered'],
        'new_recovered': item['NewRecovered'],
        'active_cases': item['ActiveCases'],
    }
    new_world_data.append(data)


@app.route("/search", methods=["POST"])
def search():
  search_term = request.form.get("search_term")
  search_results = []
  for item in new_stats_list:
    if search_term in item.values():
      search_results.append(item)
  return render_template("search_results.html", search_results=search_results, title= 'Search Data')


@app.route("/")
def home():
    return render_template('index.html', title = "Home", new_world_data = new_world_data)

@app.route("/about")
def about():
    return render_template('about.html', title = "About Us")

@app.route("/statistics")
def statistics():

    def get_pagination(offset=0, per_page=10):
        return new_stats_list[offset: offset+per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(new_stats_list)
    pagination_data = get_pagination(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('statistics.html', title = "Statistics", new_stats_list = new_stats_list, pagination_data=pagination_data,page=page,per_page=per_page,pagination=pagination)

@app.route("/infection-risk")
def infection_risk():
    return render_template('infection_risk.html', title = "Infection Risk", sortByInfectionRisk = sortByInfectionRisk)

@app.route("/recovery-presentage")
def recovery_presentage():
    return render_template('recovery_presentage.html', title = "Recovery Presentage", sortByRecoveryP = sortByRecoveryP)

@app.route("/cfr")
def cfr():
    return render_template('cfr.html', title = "CFR", sortByCFR = sortByCFR)

if __name__ == "__main__":
    app.run(debug=True)

"""
flask --app app --debug run
"""