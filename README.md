# Indeed Scraper
This program is designed to scrap job offers from https://pl.indeed.com/. Scraped offers go to output.html, and are nicely represented in form of bootstrap table.
For changelog take a look at https://github.com/grzesiekdev/indeed_scraper/blob/master/CHANGELOG.md
![Indeed Web scraper](https://i.imgur.com/DVAChtO.png)

### Built With
* [Python](https://www.python.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Requests](https://requests.readthedocs.io/en/master/)
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)



## Getting Started

```
git clone https://github.com/Regorg/indeed_scraper.git
```

### Prerequisites
* Python >=3.7
* requirements.txt
```
cd indeed_scraper
pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

```
usage: python -m scraper.main.py [-h] -j JOB_NAME -l LOCATION -r RADIUS [-s SKIP] [-t]

Scraping job offers from indeed.pl

optional arguments:
  -h, --help            show this help message and exit
  -j JOB_NAME, --job_name JOB_NAME
                        Job name
  -l LOCATION, --location LOCATION
                        Location
  -r RADIUS, --radius RADIUS
                        Radius from location
  -s SKIP, --skip SKIP  Skip offers over specified amount of time
  -t, --test            Test version , that let you to check working of the
                        script offline, on dummy page in /data/
```
Then after a while, you can check output.html in /indeed_scraper/scraper

## Development usage

Fill < > parameters with specific data
```
scraper = Scraper(<job_name: str>, <location: str>, <radius: int>, <skip: int>, <is_test_version: bool>)
template = Template(scraper.offers, scraper.number_of_offers)
```

## Tests
You can find and run tests in /indeed_scraper/tests, by:
```
python test_scraper.py
```

### Additional info

## TODO
- [x] Reorganize files structure
- [x] Make find_jobs public and set_url private
- [x] Improve CLI: use argparse for taking input from users
- [x] Reorganize Scraper class to make it easier for maintain
- [ ] Use typing lib
