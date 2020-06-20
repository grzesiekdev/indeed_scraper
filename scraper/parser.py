import argparse


class ArgParse:
    def __init__(self):
        pass

    @staticmethod
    def parse_args() -> object:
        parser = argparse.ArgumentParser(description='Scraping job offers from\
         indeed.pl')
        parser.add_argument('-j', '--job_name', type=str, help='Job name',
                            required=True)
        parser.add_argument('-l', '--location', type=str, help='Location',
                            required=True)
        parser.add_argument('-r', '--radius', type=int, help='Radius\
                            from location', required=True)
        parser.add_argument('-s', '--skip', type=int, help='Skip offers\
                            over specified amount of time', required=False)
        parser.add_argument('-t', '--test', help='Test version\
                            , that let you to check working of the script\
                             offline, on dummy page in /data/',
                            action='store_true')
        return parser.parse_args()
