from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import requests

app = Flask(__name__)

url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"
endpoint_countries = 'countries'
endpoint_world = 'world'

headers = {
    "X-RapidAPI-Key": "45f3db60cemsh852aa24317a3125p1aa9a1jsna01b5be57c21",
    "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
}

response_stats = requests.request("GET", url + endpoint_countries, headers=headers)
response_world = requests.request("GET", url + endpoint_world, headers=headers)

# Convert from json to python format 
stats_data = response_stats.json()
world_data = response_world.json()

# Filter and map stats_data into new list using map and filter
new_stats_list = list(
    map(
        lambda item: {
            'country': item['Country'],
            'total_cases': item['TotalCases'],
            'total_deaths': item['TotalDeaths'],
            'total_recovered': item['TotalRecovered'],
            'active_cases': item['ActiveCases'],
            'population': item['Population'],
            'cfr': item['Case_Fatality_Rate'],
            'recovery_presentage': item['Recovery_Proporation'],
            'infection_risk': item['Infection_Risk'],
        },
        filter(
            lambda item: item['Country'] is not None,
            stats_data
        )
    )
)
print(new_stats_list)

# Sort new_stats_list using sorted
sort_by_cfr = sorted(new_stats_list, key=lambda x: x['cfr'], reverse=True)
sort_by_recovery_p = sorted(new_stats_list, key=lambda x: x['recovery_presentage'], reverse=True)
sort_by_infection_risk = sorted(new_stats_list, key=lambda x: x['infection_risk'], reverse=True)

# Map world_data into new list using map
new_world_data = list(
    map(
        lambda item: {
            'total_cases': item['TotalCases'],
            'new_cases': item['NewCases'],
            'total_deaths': item['TotalDeaths'],
            'total_recovered': item['TotalRecovered'],
            'active_cases': item['ActiveCases'],
        },
        world_data
    )
)

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
    return render_template('infection_risk.html', title = "Infection Risk", sort_by_infection_risk = sort_by_infection_risk)

@app.route("/recovery-presentage")
def recovery_presentage():
    return render_template('recovery_presentage.html', title = "Recovery Presentage", sort_by_recovery_p = sort_by_recovery_p)

@app.route("/cfr")
def cfr():
    return render_template('cfr.html', title = "CFR", sort_by_cfr = sort_by_cfr)

if __name__ == "__main__":
    app.run(debug=True)