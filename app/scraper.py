import time
from datetime import datetime, date, timedelta

from github import Github

from config import config


def generate_dates(d1, d2, return_format="str", date_format="%Y-%m-%d"):
    d1 = datetime.strptime(d1, date_format)
    d2 = datetime.strptime(d2, date_format)
    delta = d2 - d1
    for i in range(delta.days + 1):
        date = d1 + timedelta(days=i)
        if return_format == "str":
            yield datetime.strftime(date, date_format)
        else:
            yield date


class GithubRepoScraper():
    def __init__(self, d1, d2, sort="stars", order="desc", per_page=30,
            **qualifiers):
        self._d1 = d1
        self._d2 = d2
        self._sort = sort
        self._order = order
        self._query = ' '.join(qualifiers.values())
        self._gh = Github(config['default'].GITHUB_ID,
                config['default'].GITHUB_TOKEN)
        self._gh.per_page = per_page

    def wait(self):
        reset_time = self._gh.rate_limiting_resettime
        wait_time = int(reset_time - time.time()) + 2
        print("Resume at {}".format(datetime.fromtimestamp(reset_time)))
        time.sleep(wait_time)

    def _scrape(self, date):
        if not self._gh.rate_limiting[0]:
            self.wait()
        query = ' '.join([self._query, "created:" + date])
        repos = self._gh.search_repositories(query, sort=self._sort,
                order=self._order)
        total = 0
        count = 0
        for repo in repos:
            total += 1
            if not self._gh.rate_limiting[0]:
                count += 1
                if count >= self._gh.per_page:
                    count = 0
                    self.wait()
        print("DONE: {0}: {1} items scraped".format(date, total))

    def scrape(self):
        print("Ratelimit: {}".format(self._gh.rate_limiting))
        for date in generate_dates(self._d1, self._d2):
            self._scrape(date)

ghrs = GithubRepoScraper(d1='2011-01-01', d2='2015-03-01',
        keywords="android",
        fields="in:name,description,readme",
        language="language:Java")
ghrs.scrape()
