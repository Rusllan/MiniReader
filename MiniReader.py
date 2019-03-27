import requests
from bs4 import BeautifulSoup
import textwrap


def get_html(url):
    r = requests.get(url)
    return r.text


class Article:

    def __init__(self, url):
        self.soup = BeautifulSoup(get_html(url), features="html.parser")
        self.blocks = self.soup.find_all(['p', 'h1', 'h2', 'h3'])

    def print(self):
        for block in self.blocks:
            print(textwrap.fill(block.text, 80))
            print()


def main():
    url = 'https://meduza.io/slides/prishlos-120-chasov-podmetat-pol-i-myt-tramvai-v-transportnom-depo'

    article = Article(url)
    article.print()


if __name__ == '__main__':
    main()
