import requests
from bs4 import BeautifulSoup
import re
import math
import sys


class Scraper:
    def __init__(self, job_name, location, radius, skip, is_test_version):
        self.job_name = job_name
        self.location = location
        self.radius = radius
        self.skip = skip
        self.is_test_version = is_test_version

        self._url = ''
        self.page = None
        self.page_number = 0

        self.soup = None
        self.result = None

        self.get_content()
        self.offers = {}
        self.number_of_offers = 0

    def show_link(self) -> None:
        print(f'URL: {self._url}, Place: {self.location}, Job name: \
{self.job_name}\n')

    def get_url(self) -> str:
        return self._url

    def __set_url(self, url: str) -> None:
        self._url = url

    def __set_to_test_mode(self) -> None:
        with open('data/sample_page.html', 'r') as f:
            self.page = f.read()
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.result = self.soup.find(id='resultsCol')

    def __set_to_normal_mode(self) -> None:
        self.page = self.connect(f'https://pl.indeed.com/jobs?q=\
{self.job_name}&l={self.location}&sort=date&radius={self.radius}\
&start={self.page_number}')
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.result = self.soup.find(id='resultsCol')

    def connect(self, url: str) -> object:
        try:
            self.__set_url(url)
            connection = requests.get(self.get_url())
            return connection
        except requests.exceptions.RequestException as e:
            return e

    def get_content(self) -> None:
        if self.is_test_version:
            self.__set_to_test_mode()
        else:
            self.__set_to_normal_mode()

    def find_jobs_div(self) -> str:
        return self.result.find_all('div', class_='jobsearch-SerpJobCard')

    def add_to_offers(self, title: str, company: str, location: str, date: str,
                      link: str) -> None:
        self.offers[title.text.strip()] = {
            'company': company.text.strip(),
            'location': location.text.strip(),
            'date': date.text.strip(),
            'link': "https://pl.indeed.com" + str(link)
        }

    def find_number_of_pages(self) -> int:
        pages = self.soup.find(id='searchCountPages')
        if not pages:
            return False
        text = pages.text.strip()

        # indeed display 15 offers on single page, that's why i divide by 15
        number_of_pages = int(re.findall(r'\d+', text)[1])
        return math.ceil(number_of_pages / 15)

    def update_pages(self, pages: int) -> list:
        pages_urls = []
        for i in range(pages):
            counter = i * 10
            pages_urls.append(counter)
        return pages_urls

    def check_and_get_location(self, location: str, job: object) -> tuple:
        if not location:
            location = job.find('span', class_='location')
            if not location:
                return False, None
        return True, location

    def is_over30_skipped(self, date: str) -> bool:
        if not self.skip:
            self.skip = 40
        exceptions = ['Dodano dzisiaj', 'wczoraj', 'Dodano przed chwilą']
        if date.text.strip() in exceptions:
            return False
        if int(date.text.strip()[:2]) / 10 < 1 and self.skip >= 10:
            return False
        else:
            if int(date.text.strip()[:2]) > self.skip:
                return True
            else:
                return False

    def find_job_offers(self) -> None:
        pages = self.find_number_of_pages()
        if not pages:
            print('No offers found! Try to change your query.')
            return

        pages_updated = self.update_pages(pages)

        for page in pages_updated:
            self.page_number = page
            self.get_content()
            jobs = self.find_jobs_div()
            for job in jobs:
                title = job.find('h2', class_='title')
                company = job.find('span', class_='company')
                location = job.find('div', class_='location')
                date = job.find('span', class_='date')
                link = job.find('a')['href']

                is_location, location = self.check_and_get_location(location,
                                                                    job)

                if not is_location or self.is_over30_skipped(date):
                    continue

                if None in (title, company, location, date, link):
                    print("Something went wrong, offer skipped...")
                    continue

                self.add_to_offers(title, company, location, date, link)
                self.number_of_offers += 1
        print("Done! Go check output.html")

    def __repr__(self) -> str:
        return f'Scraper object with {self.get_url()} URL'
