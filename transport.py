import bs4


class Transport:
    def __init__(self, init_name: str = None, init_color = None) -> None:
        self.name = init_name
        self.color = init_color


    def set_info(self, trpt_html: bs4.element.Tag):
        """
        `trpt_html`: `<li class="transport"> </li>`
        """
        self.name = trpt_html.get_text().replace('[line]', '')
        if '[lineWalk]' in trpt_html.get_text():
            self.color = trpt_html.find('span', class_='lineWalk')['style'].replace('border-left-color:', '')
            self.name = trpt_html.get_text().replace('[lineWalk]', '')
        else:
            self.color = trpt_html.find('span', class_='line')['style'].replace('border-left-color:', '')
