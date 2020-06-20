from scraper import Scraper
from template import Template
from parser import ArgParse


def start_scraping():
    args = ArgParse.parse_args()
    job_name = args.job_name
    location = args.location
    radius = args.radius
    skip = args.skip
    is_test_version = args.test

    scraper = Scraper(job_name, location, radius, skip, is_test_version)
    scraper.show_link()
    scraper.find_job_offers()

    template = Template(scraper.offers, scraper.number_of_offers)


if __name__ == '__main__':
    start_scraping()
