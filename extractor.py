import re
from requests import get
from requests.exceptions import MissingSchema, ConnectionError
import pandas as pd


class Extractor:

    def __init__(self, regular_expression):

        self.regular_expression = regular_expression
        self.elements = set()

    def find_elements(self, text):

        new_elements = set(re.findall(
            self.regular_expression, text, re.I))

        return new_elements

    def extract_from_url(self, url):

        try:
            response = get(url)
        except (MissingSchema, ConnectionError):
            print("Somethind went wrong openning the url")

        new_elements = self.find_elements(response.text)
        self.elements.update(new_elements)

    def extract_from_file(self, file):


        with open(file, 'r') as infile:
            all_data = infile.read()
            new_elements = self.find_elements(all_data)

        self.elements.update(new_elements)

    def save_results(self, path, filename):

        df = pd.DataFrame(self.elements, columns=[filename])
        df.to_csv(f'{path}/{filename}.csv', index=False)


if __name__ == '__main__':

    # # url = 'https://github.com/nataMamed/WebScraping/blob/main/data/emails_rgs.csv'

    # # reg = r'\w+@\w+\.{1}\w+'
    # # reg2 = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com"
    # name = 'cirobastos'
    # reg3 = name + '+@\w+\.{1}\w+'
    # email_extractor = Extractor(reg3)

    # email_extractor.extract_from_file('/home/natamamede/Documentos/python_projects/Mobills/Mobills/data/emails_rgs.csv')
    # print(email_extractor.elements)
    # email_extractor.extract_from_url(url)
    # print(email_extractor.elements)

    # email_extractor.save_results('results', 'emails')
    # emails_rgs = pd.read_csv('data/emails_rgs.csv')
    # emails_rgs['server'] = [email.split('@')[1] for email in emails_rgs.email]
    # emails_rgs['user'] = [email.split('@')[0] for email in emails_rgs.email]


    # search = emails_rgs[emails_rgs['user'] == 'viniciusbrasil']