import requests
from bs4 import BeautifulSoup
import textwrap


def get_html(url):
    r = requests.get(url)
    return r.text


def main():
    url = 'https://meduza.io/slides/prishlos-120-chasov-podmetat-pol-i-myt-tramvai-v-transportnom-depo'
    soup = BeautifulSoup(get_html(url), features="html.parser")

    blocks = soup.find_all(['p', 'h1', 'h2', 'h3'])

    for block in blocks:
        print(textwrap.fill(block.text, 80))
        print()


if __name__ == '__main__':
    main()
