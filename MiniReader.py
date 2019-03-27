import argparse
import os
import requests
from bs4 import BeautifulSoup
import textwrap


def get_html(url):
    r = requests.get(url)
    return r.text


class Article:

    def __init__(self, url):
        self.url = url
        self.tags_to_read = ['p', 'h1', 'h2', 'h3']

        self.text = self.text_from_html(get_html(self.url))

    def text_from_html(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        blocks = soup.find_all(self.tags_to_read)
        text = ''

        for block in blocks:
            text += textwrap.fill(block.text, 80) + '\n\n'
        return text

    def save(self):

        if self.url.startswith('http://'):
            cleaned_url = self.url[7:]
        elif self.url.startswith('https://'):
            cleaned_url = self.url[8:]
        else:
            cleaned_url = self.url

        folders = cleaned_url.split('/')[:-1]
        path = './'
        for i, folder in enumerate(folders):
            path += folder + '/'
            if not os.path.exists(path):
                os.mkdir(path)

        filename = cleaned_url.split('/')[-1].split('.')[0] + '.txt'
        with open(path + filename, 'w') as file:
            file.write(self.text)


def main():
    url = 'https://meduza.io/slides/prishlos-120-chasov-podmetat-pol-i-myt-tramvai-v-transportnom-depo'

    article = Article(url)
    print(article.text)
    article.save()


if __name__ == '__main__':
    main()
