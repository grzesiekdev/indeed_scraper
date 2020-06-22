class JobOffer:
    def __init__(self, job):
        self.job = job
        self.title = ''
        self.company = ''
        self.location = ''
        self.date = ''
        self.link = ''
        self.offers = {}

    def get_attibutes(self, job):
        title = job.find('h2', class_='title').text.strip()
        company = job.find('span', class_='company').text.strip()
        location = job.find('div', class_='location')
        date = job.find('span', class_='date').text.strip()
        link = str(job.find('a')['href'])
        self.add_to_offers(title, company, location, date, link)

    def add_to_offers(self, title: str, company: str, location: str, date: str,
                      link: str) -> None:
        self.offers[title] = {
            'company': company,
            'location': location,
            'date': date,
            'link': f'https://pl.indeed.com{link}'
        }

    def __str__(self):
        return f'Job offer: {job}'
