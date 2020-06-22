import requests
from bs4 import BeautifulSoup  # type: ignore
import re
import math
import sys
import logging
from job import JobOffer  # type: ignore


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

        self.number_of_offers = 0
        self.offers = {}

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

    def find_number_of_pages(self) -> int:
        pages = self.soup.find(id='searchCountPages')
        if not pages:
            return 0
        text = pages.text.strip()

        # indeed display 15 offers on single page, that's why i divide by 15
        number_of_pages = int(re.findall(r'\d+', text)[1])
        return math.ceil(number_of_pages / 15)

    def get_pages(self, pages: int) -> list:
        if not pages:
            print("0 offers found! Try to change your query")
            return []
        else:
            return [i for i in range(0, pages*10, 10)]

    def find_job_offers(self) -> None:
        pages = self.get_pages(self.find_number_of_pages())

        for page in pages:
            self.page_number = page
            self.get_content()
            jobs = self.find_jobs_div()
            for job in jobs:
                offer = JobOffer(job, self.skip)
                offer.get_attibutes()
                offer.process_jobs()
                if offer.continue_loop:
                    continue
                else:
                    offer.add_to_offers()
                    self.offers.update(offer.offers)
                self.number_of_offers += 1
        print("Done! Go check output.html")

    def __str__(self) -> str:
        return f'Scraper object with {self.url()} URL'
