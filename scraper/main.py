#!/usr/bin/python
from . import scraper
from . import template  # type: ignore
from . import parser  # type: ignore


def start_scraping():
    args = parser.ArgParse.parse_args()
    job_name = args.job_name
    location = args.location
    radius = args.radius
    skip = args.skip
    is_test_version = args.test

    scraper = scraper.Scraper(
                            job_name,
                            location,
                            radius,
                            skip,
                            is_test_version
                        )
    scraper.get_content()
    print(scraper.show_info())
    scraper.find_job_offers()
    template = template.Template(scraper.offers, scraper.number_of_offers)


if __name__ == '__main__':
    start_scraping()
