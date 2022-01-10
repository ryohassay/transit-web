from typing import Dict, List
from flask import Flask, render_template, request
from datetime import datetime as dt
from datetime import time as tm

from route import RouteSearch, Route

app = Flask(__name__)


def _convert_tm_type(tm_type_str):
    if tm_type_str == 'dep':
        tm_type = 1
    elif tm_type_str == 'arr':
        tm_type = 4
    elif tm_type_str == 'las':
        tm_type = 2
    elif tm_type_str == 'fir':
        tm_type = 3
    elif tm_type_str == 'non' or tm_type_str == '':
        tm_type = 5
    else:
        raise ValueError('The value of `tm_type` is not valid.')

    return tm_type


def _search_transit(start: str, dest: str, tm: dt, tm_type: int):
    route = Route(RouteSearch(start, dest, tm, tm_type))
    route.search.search()
    route.get_summary()
    route.get_detail()
    return route


def _convert_route_for_js(route: Route) -> List[Dict]:
    stations_js = []
    for station in route.stations:
        station_js = {
            "name": station.name,
            "dep_tm": station.dep_tm,
            "arr_tm": station.arr_tm
        }
        stations_js.append(station_js)

    transports_js = []
    for transport in route.transports:
        transport_js = {
            "name": transport.name,
            "color": transport.color
        }
        transports_js.append(transport_js)

    route_js = {
        "start": route.start,
        "dest": route.dest,
        "dep_tm": route.dep_tm,
        "arr_tm": route.arr_tm,
        "fare": route.fare,
        "stations": stations_js,
        "transports": transports_js,
        "url": route.search.url
    }

    return route_js


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/", methods=['post'])
def result():
    routes_js = []
    for i in range(5):
        ip_start = request.form["ip[{}]['start']".format(i)]
        ip_dest = request.form["ip[{}]['dest']".format(i)]
        ip_tm_type = request.form["ip[{}]['tm_type']".format(i)]
        ip_date = request.form["ip[{}]['date']".format(i)]
        ip_time = request.form["ip[{}]['time']".format(i)]

        if ip_start != "" and ip_dest != "":
            if ip_time == '':
                ip_dt = dt.now()
            elif ip_date == '':
                today = dt.today()
                time = tm.fromisoformat(ip_time)
                ip_dt = dt.combine(today, time)
            else:
                ip_dt = dt.strptime('{} {}'.format(ip_date, ip_time), '%Y-%m-%d %H:%M')

            ip_tm_type_int = _convert_tm_type(ip_tm_type)
            route = _search_transit(ip_start, ip_dest, ip_dt, ip_tm_type_int)

            # Rearrange the object to list of dictionaries
            route_js = _convert_route_for_js(route)
            routes_js.append(route_js)

    return render_template("results.html", routes=routes_js)
    # return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
