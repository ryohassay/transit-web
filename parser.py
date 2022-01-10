import argparse


class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', '--debug', default=False, help='debug')
        self.parser.add_argument('--host', default='0.0.0.0', help='host')
        self.args = self.parser.parse_args()


    def get_args(self) -> argparse.Namespace:
        return self.args
