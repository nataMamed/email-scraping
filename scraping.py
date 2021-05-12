import re
from requests import get
from requests.exceptions import MissingSchema, ConnectionError
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd


class ExtractEmails:

    def __init__(self, urls: list):

        self.unscraped = deque(urls)
        self.scraped   = set()
        self.emails    = set()

    @staticmethod
    def extract_path(parts, url):
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url

        return path

    @staticmethod
    def find_emails(response):

        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))

        return new_emails

    def extract_extra_links(self, response, base_url, path):

        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
            if "href" in anchor.attrs:
                link = anchor.attrs["href"]
            else:
                link = ''

                if link.startswith('/'):
                    link = base_url + link

                elif not link.startswith('http'):
                    link = path + link

                if not link.endswith(".gz"):
                    if not link in self.unscraped and not link in self.scraped:
                        self.unscraped.append(link)

    def make_scraping(self):

        while len(self.unscraped):
            url = self.unscraped.popleft()
            self.scraped.add(url)

            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)

            path = self.extract_path(parts, url)

            try:
                response = get(url)
            except (MissingSchema, ConnectionError):
                continue

            new_emails = self.find_emails(response)
            self.emails.update(new_emails)

            self.extract_extra_links(response, base_url, path)

    def save_results(self, path):

        df = pd.DataFrame(self.emails, columns=["Email"])
        df.to_csv(f'{path}/email.csv', index=False)


urls = [' https://pt.wikihow.com/Criar-Contas-de-E-mail-M%C3%BAltiplas',
        ' https://pt.wikihow.com/Criar-Contas-de-E-mail-M%C3%BAltiplas']

extractor = ExtractEmails(urls)
extractor.make_scraping()
extractor.save_results('results')
