import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
import textwrap


def get_html(url):
    request = requests.get(url)
    return request.text


class Article:

    def __init__(self, url):
        self.url = url
        setup = self.load_setup()
        self.tags_to_find = setup['tags_to_find']
        self.classes_to_ignore = setup['classes_to_ignore']
        self.classes_to_include = setup['classes_to_include']
        self.show_links = setup['show_links']

        self.text = self.text_from_html(get_html(self.url))

    @staticmethod
    def load_setup():
        with open('setup.json', 'r') as setup_file:
            setup = json.load(setup_file)
        return setup

    def text_from_html(self, html):
        soup = BeautifulSoup(html, features="html.parser")

        ignore_tags = soup.find_all(True, {'class': self.classes_to_ignore})
        for ignore_tag in ignore_tags:
            ignore_tag.decompose()

        if self.show_links:
            for a in soup.findAll('a'):
                if a.has_attr('href') and 'http' in a['href']:
                    a.replace_with('{}[{}]'.format(a.text, a['href']))

        tags = []
        if soup.find(class_=self.classes_to_include):
            tags += soup.find_all('h1')
            tags += soup.find_all(True, {'class': self.classes_to_include})
            for found_tag in soup.findAll(self.tags_to_find):
                found_tag.replace_with('{}\n'.format(found_tag.text))
        else:
            tags += soup.find_all(self.tags_to_find)
        text = ''

        for tag in tags:
            for block in tag.text.split('\n'):
                if block not in ['', '\r']:
                    text += textwrap.fill(b, 80) + '\n\n'
        return text

    def save(self):

        if self.url.startswith('http://'):
            cleaned_url = self.url[7:]
        elif self.url.startswith('https://'):
            cleaned_url = self.url[8:]
        else:
            cleaned_url = self.url

        if cleaned_url[-1] == '/':
            cleaned_url = cleaned_url[:-1]

        folders = cleaned_url.split('/')[:-1]
        path = './'
        for folder in folders:
            path += folder + '/'
            if not os.path.exists(path):
                os.mkdir(path)

        filename = cleaned_url.split('/')[-1].split('.')[0] + '.txt'
        with open(path + filename, 'w') as file:
            file.write(self.text)


def main():
    parser = argparse.ArgumentParser(description='Little utility for creation easy to read txt files from web pages.')
    parser.add_argument('url', help='Url from which text will be formed.')
    args = parser.parse_args()

    article = Article(args.url)
    print(article.text)
    article.save()


if __name__ == '__main__':
    main()
