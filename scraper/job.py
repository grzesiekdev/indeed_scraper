class JobOffer():
    def __init__(self, job, skip):
        self.job = job
        self.skip = skip
        self.title = ''
        self.company = ''
        self.location = ''
        self.date = ''
        self.link = ''
        self.offers = {}
        self.continue_loop = False

    def get_attibutes(self) -> None:
        self.title = self.job.find('h2', class_='title').text.strip()
        self.company = self.job.find('span', class_='company').text.strip()
        self.location = self.job.find('div', class_='location')
        self.date = self.job.find('span', class_='date').text.strip()
        self.link = str(self.job.find('a')['href'])

    def add_to_offers(self) -> dict:
        self.offers[self.title] = {
            'company': self.company,
            'location': self.location,
            'date': self.date,
            'link': f'https://pl.indeed.com{self.link}'
        }
        return self.offers

    def check_and_set_location(self) -> bool:
        print(self.location)
        if not self.location:
            self.location = self.job.find('span', class_='location')
            if not self.location:
                return False
        return True

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

    def process_jobs(self) -> None:
        self.check_and_set_location()
        self.continue_loop = False
        if not self.location or self.are_older_offers_skipped(self.date):
            self.continue_loop = True
        exceptions = [
                    self.title,
                    self.company,
                    self.location,
                    self.date,
                    self.link
                    ]
        if None in exceptions:
            self.continue_loop = True
        else:
            self.location = self.location.text.strip()

    def __str__(self):
        return f'Job offer: {job}'
