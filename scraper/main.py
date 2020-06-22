#!/usr/bin/python
import scraper as sc
import template as tp  # type: ignore
import parser  # type: ignore


def start_scraping():
    args = parser.ArgParse.parse_args()
    job_name = args.job_name
    location = args.location
    radius = args.radius
    skip = args.skip
    is_test_version = args.test

    scraper = sc.Scraper(
                            job_name,
                            location,
                            radius,
                            skip,
                            is_test_version
                            )
    scraper.get_content()
    scraper.show_link()
    scraper.find_job_offers()
    template = tp.Template(scraper.offers, scraper.number_of_offers)


if __name__ == '__main__':
    start_scraping()
