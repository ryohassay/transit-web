from datetime import time
import requests, re
from bs4 import BeautifulSoup

from station import Station
from transport import Transport
from route import RouteSearch, Route

# for data type annotation
import bs4
from typing import List


if __name__ == '__main__':
    total_fare = 0
    while True:
        start = input('出発駅を入力してください：')
        if start == '':
            break
        dest = input('到着駅を入力してください：')

        route = Route(RouteSearch(start, dest))
        route.search.search()
        route.get_summary()

        print('運賃：{}円\n'.format(route.fare))
        total_fare += route.fare

        route.get_detail()
        route.show_detail()

    print('合計運賃：{}円'.format(total_fare))
