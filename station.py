import bs4


class Station:
    def __init__(self, init_name: str = None, init_dep_tm: str = None, init_arr_tm: str = None) -> None:
        self.name = init_name
        self.dep_tm = init_dep_tm
        self.arr_tm = init_arr_tm


    def set_info(self, sta_html: bs4.element.Tag, has_time: bool):
        """
        `sta_html`: `<div class="station"> </div>`
        """

        self.name = sta_html.find('dt').get_text()
        if has_time:
            time_htmls = sta_html.find('ul', class_='time').find_all('li')
            times = [time_html.get_text() for time_html in time_htmls]
            if len(times) == 1:
                sta_status = sta_html.find('img')['alt']
                if sta_status == '出発駅':
                    self.dep_tm = times[0]
                elif sta_status == '到着駅':
                    self.arr_tm = times[0]
                else:
                    raise ValueError('Function could not get deperture or arrival time properly.')
            elif len(times) == 2:
                self.arr_tm = times[0].replace('着', '')
                self.dep_tm = times[1].replace('発', '')
            else:
                raise ValueError('Function could not get deperture and arrival time properly.')
