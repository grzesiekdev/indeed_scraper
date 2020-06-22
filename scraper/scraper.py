import requests
from bs4 import BeautifulSoup  # type: ignore
import re
import math
import sys
import logging


class Scraper:
    def __init__(self, job_name, location, radius, skip, is_test_version):
        self.job_name = job_name
        self.location = location
        self.radius = radius
        self.skip = skip
        self.is_test_version = is_test_version

        self.url = ''
        self.page = None
        self.page_number = 0

        self.soup = None
        self.result = None

        self.offers = {}
        self.number_of_offers = 0

        logging.basicConfig(
            filename='logs/log.log',
            filemode='w',
        )

    def show_link(self) -> None:
        print(f'URL: {self.url}, Place: {self.location}, Job name: \
{self.job_name}\n')

    def __set_to_test_mode(self) -> None:
        with open('data/sample_page.html', 'r') as f:
            self.page = f.read()
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.result = self.soup.find(id='resultsCol')

    def __set_to_normal_mode(self) -> None:
        url = (
            'https://pl.indeed.com/jobs?'
            f'q={self.job_name}&'
            f'l={self.location}&'
            'sort=date&'
            f'radius={self.radius}&'
            f'start={self.page_number}'
        )
        try:
            self.page = self.connect(url)
        except requests.exceptions.RequestException as e:
            print("Error occured! Go check logs/log.log for more informations")
            logging.error(e)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.result = self.soup.find(id='resultsCol')

    def connect(self, url: str) -> object:
        self.url = url
        connection = requests.get(self.url)
        return connection

    def get_content(self) -> None:
        if self.is_test_version:
            self.__set_to_test_mode()
        else:
            self.__set_to_normal_mode()

    def find_jobs_div(self) -> str:
        return self.result.find_all('div', class_='jobsearch-SerpJobCard')

    def add_to_offers(self, title: str, company: str, location: str, date: str,
                      link: str) -> None:
        self.offers[title] = {
            'company': company,
            'location': location,
            'date': date,
            'link': f'https://pl.indeed.com{link}'
        }

    def find_number_of_pages(self) -> int:
        pages = self.soup.find(id='searchCountPages')
        if not pages:
            return 0
        text = pages.text.strip()

        # indeed display 15 offers on single page, that's why i divide by 15
        number_of_pages = int(re.findall(r'\d+', text)[1])
        return math.ceil(number_of_pages / 15)

    def get_pages(self, pages: int) -> list:
        return [i for i in range(0, pages*10, 10)]

    def check_and_get_location(self, location: str, job) -> object:
        if not location:
            location = job.find('span', class_='location').text.strip()
            if not location:
                return False
        return location

    def are_older_offers_skipped(self, date: str) -> bool:
        if not self.skip:
            self.skip = 40
        exceptions = ['Dodano dzisiaj', 'wczoraj', 'Dodano przed chwilą']
        if date in exceptions:
            return False
        if int(date[:2]) / 10 < 1 and self.skip >= 10:
            return False
        else:
            if int(date[:2]) > self.skip:
                return True
            else:
                return False

    def process_jobs(self, attributes: dict, job):
        title = attributes['title']
        company = attributes['company']
        location = attributes['location']
        date = attributes['date']
        link = attributes['link']

        location = self.check_and_get_location(location, job)
        if not location or self.are_older_offers_skipped(date):
            return ''
        location = location.text.strip()
        if None in (title, company, location, date, link):
            return ''
        else:
            return attributes

    def get_attributes_from_job_offer(self, job) -> dict:
        title = job.find('h2', class_='title').text.strip()
        company = job.find('span', class_='company').text.strip()
        location = job.find('div', class_='location')
        date = job.find('span', class_='date').text.strip()
        link = str(job.find('a')['href'])

        return {
                'title': title,
                'company': company,
                'location': location,
                'date': date,
                'link': link
                }

    def find_job_offers(self) -> None:
        pages = self.find_number_of_pages()
        if not pages:
            print('No offers found! Try to change your query.')
            return

        pages_updated = self.get_pages(pages)

        for page in pages_updated:
            self.page_number = page
            self.get_content()
            jobs = self.find_jobs_div()
            for job in jobs:
                attributes = self.get_attributes_from_job_offer(job)
                attributes = self.process_jobs(attributes, job)
                title = attributes['title']
                company = attributes['company']
                location = attributes['location']
                date = attributes['date']
                link = attributes['link']
                self.add_to_offers(title, company, location, date, link)
                self.number_of_offers += 1
        print("Done! Go check output.html")

    def __str__(self) -> str:
        return f'Scraper object with {self.url()} URL'
