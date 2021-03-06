import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from scraper.scraper import Scraper
from scraper.job import JobOffer
import unittest
os.chdir('..')


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper('python', 'katowice', 15, 20, False)
        self.scraper_local = Scraper('python', 'katowice', 15, 20, True)
        self.scraper.get_content()
        self.scraper_local.get_content()
        """
        Creating second scraper object which works without requests,
        but with static page in /data/ - i am checking with it adding to dicts,
        which seems hard to implement with requests. Also, it's helpful to test
        scraping page structure. Of course it won't help when page structure
        changes.
        """
        self.job = self.scraper_local.find_jobs_div()[0]
        self.offer = JobOffer(self.job, self.scraper_local.skip)


class TestInit(TestMain):
    def test_init(self) -> None:
        self.assertEqual(self.scraper.job_name, 'python')
        self.assertEqual(self.scraper.location, 'katowice')
        self.assertEqual(self.scraper.radius, 15)

        self.assertEqual(self.scraper.url, 'https://pl.indeed.com/\
jobs?q=python&l=katowice&sort=date&radius=15&start=0')
        self.assertEqual(str(self.scraper.page), '<Response [200]>')


class TestScraper(TestMain):
    def test_find_number_of_pages(self) -> None:
        number_of_pages = self.scraper_local.find_number_of_pages()
        self.assertEqual(number_of_pages, 11)

    def test_get_pages(self) -> None:
        number_of_pages = self.scraper_local.find_number_of_pages()
        urls = self.scraper_local.get_pages(number_of_pages)

        self.assertEqual(urls, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

    def test_show_info(self) -> None:
        info = ('URL: https://pl.indeed.com/'
                'jobs?q=python&l=katowice&sort=date&'
                'radius=15&start=0,Place: katowice,Job name: python\n'
                )
        self.assertEqual(self.scraper.show_info(), info)

    def test_connect(self) -> None:
        self.assertEqual(str(self.scraper.connect(self.scraper.url)),
                         '<Response [200]>')

    def test_find_jobs_div(self) -> None:
        status = self.scraper_local.find_jobs_div()
        self.assertTrue(status)


class TestJobOffer(TestMain):
    def test_get_attributes(self) -> None:
        self.offer.get_attibutes()
        self.offer.process_jobs()
        self.assertEqual(self.offer.title, 'Software Engineer')
        self.assertEqual(self.offer.company, 'Bombardier')
        self.assertEqual(self.offer.location, 'Katowice, śląskie')
        self.assertEqual(self.offer.date, 'Dodano dzisiaj')
        self.assertEqual(self.offer.link, '/rc/clk?jk=b3061858992c678a&fccid=b\
3f8eab3b50969f8&vjs=3')

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

    def test_check_and_set_location(self) -> None:
        self.assertTrue(self.offer.check_and_set_location())


if __name__ == '__main__':
    unittest.main()
