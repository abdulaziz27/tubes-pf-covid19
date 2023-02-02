from flask import Flask, render_template, url_for, request
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
        'total_case': item['TotalCases'],
        #'new_cases': item['NewCases'],
        'total_death': item['TotalDeaths'],
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


@app.route("/search", methods = ['POST', 'GET'])
def search():  
    return render_template('navbar.html', title = 'Search Data')

@app.route("/")
def home():
    return render_template('index.html', title = "Home", new_world_data = new_world_data)

@app.route("/about")
def about():
    return render_template('about.html', title = "About")

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title = "Statistics", stats_list = new_stats_list)

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