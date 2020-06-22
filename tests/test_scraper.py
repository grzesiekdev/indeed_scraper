import sys
import os
# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from scraper.scraper import Scraper
import unittest


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        # os.chdir('../scraper')
        self.scraper = Scraper('python', 'katowice', 15, 20, False)
        self.scraper_local = Scraper('python', 'katowice', 15, 20, True)
        self.scraper.get_content()
        self.scraper_local.get_content()
        """
        Creating scraper object from ScraperLocal which works without requests,
        but with static page in /data/ - i am checking with it adding to dicts,
        which seems hard to implement with requests. Also, it's helpful to test
        scraping page structure. Of course it won't help when page structure
        changes.
        """


class TestInit(TestMain):
    def test_init(self) -> None:
        self.assertEqual(self.scraper.job_name, 'python')
        self.assertEqual(self.scraper.location, 'katowice')
        self.assertEqual(self.scraper.radius, 15)

        self.assertEqual(self.scraper.url, 'https://pl.indeed.com/\
jobs?q=python&l=katowice&sort=date&radius=15&start=0')
        self.assertEqual(str(self.scraper.page), '<Response [200]>')


class TestScraper(TestMain):
    def test_add_to_offers(self) -> None:
        self.scraper_local.find_job_offers()
        self.assertEqual(self.scraper_local.offers['Software Engineer']
                         ['company'], 'Bombardier')
        self.assertEqual(self.scraper_local.offers['Software Engineer']
                         ['location'], 'Katowice, śląskie')
        self.assertEqual(self.scraper_local.offers['Software Engineer']
                         ['date'], 'Dodano dzisiaj')
        self.assertEqual(self.scraper_local.offers['Software Engineer']
                         ['link'], 'https://pl.indeed.com/rc/clk?jk=\
b3061858992c678a&fccid=b3f8eab3b50969f8&vjs=3')

    def test_find_number_of_pages(self) -> None:
        number_of_pages = self.scraper_local.find_number_of_pages()
        self.assertEqual(number_of_pages, 11)

    def test_get_pages(self) -> None:
        number_of_pages = self.scraper_local.find_number_of_pages()
        urls = self.scraper_local.get_pages(number_of_pages)

        self.assertEqual(urls, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    def test_is_location_set(self) -> None:
        jobs = self.scraper_local.find_jobs_div()
        for job in jobs:
            location = job.find('div', class_='location')
            location = self.scraper_local.check_and_get_location(location,
                                                                 job
                                                                 )
        self.assertTrue(self.scraper_local.check_and_get_location(location,
                                                                  True))
        self.assertTrue(self.scraper_local.check_and_get_location(location,
                                                        'Katowice śląskie'))


if __name__ == '__main__':
    unittest.main()
