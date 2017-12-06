import requests
import re
import pandas as pd
import datetime as dt
from requests.auth import HTTPBasicAuth
from functools import reduce
from sqlalchemy import create_engine


class GitPoller():
    def __init__(self, app_config):
        self.repos = app_config['GIT_REPOS']
        self.USER = app_config['GIT_SECRET']['USER']
        self.TOKEN = app_config['GIT_SECRET']['TOKEN']
        self.DB_URI = app_config['SQLALCHEMY_DATABASE_URI']
        self.endpoints = {
            'commits': '/commits?per_page=100',
            'issues': '/issues?per_page=100'
        }
        self.polling = False
        self.page_limit = 1

        # initialize dictionaries for tracking incremental downloads
        self.last_modified = {}
        self.last_page = {}
        for repo in self.repos:
            last_modified = {}
            last_page = {}
            for endpoint in self.endpoints:
                last_modified[endpoint] = 0
                last_page[endpoint] = 0
            self.last_modified[repo] = last_modified
            self.last_page[repo] = last_page

    def _parse_datetime(last_modified):
        return dt.datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z")

    def _parse_header(self, response):
        last_modified = response.headers['Last-Modified']
        # if less than 100 items
        if 'Link' in response.headers:
            pages = response.headers['Link'].split(", ")
            next_page = [s for s in pages if 'rel="next"' in s]
            last_page = [s for s in pages if 'rel="last"' in s]
            prev_page = [s for s in pages if 'rel="prev"' in s]
            end = False

            if last_page:
                last_page_num = int(re.findall('&page=(\d+)', last_page[0])[0])
            else:
                last_page_num = int(re.findall('&page=(\d+)', prev_page[0])[0])+1

            if next_page:
                next_page_num = int(re.findall('&page=(\d+)', next_page[0])[0])
                next_url = re.findall('\<(\S+)\>', next_page[0])[0]
            else:
                end = True
                next_page_num = last_page_num
                next_url = None
        else:
            end = True
            next_url = None
            next_page_num = 1
            last_page_num = 1
        return (end, next_url, next_page_num, last_modified, last_page_num)

    def _single_repo_endpoints(self, repo, endpoint, start_page=1):
        # first request
        url = "https://api.github.com/repos/" +\
            repo + self.endpoints[endpoint] +\
            "&page=" + str(start_page)
        response = requests.get(url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
        df = pd.DataFrame(response.json())
        last_page, next_url, next_page_num, last_modified, last_page_num =\
            self._parse_header(response)

        while (not last_page) and (next_page_num <= self.page_limit):
            response = requests.get(next_url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
            last_page, next_url, next_page_num, last_modified, last_page_num =\
                self._parse_header(response)
            df = pd.concat([df, pd.DataFrame(response.json())])

        # update trackers for given repo and endpoint
        self.last_modified[repo][endpoint] = last_modified
        self.last_page[repo][endpoint] = last_page_num
        return df

    def get_rate_limit(self):
        url = "https://api.github.com/rate_limit"
        response = requests.get(url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
        return int(response.headers['X-RateLimit-Remaining'])

    def _all_repos_endpoints(self, endpoint):
        dfs = []
        for repo in self.repos:
            dfs.append(self._single_repo_endpoints(repo, endpoint))
        df = reduce(lambda left, right: pd.concat([left, right]), dfs)

        return df

    def set_page_limit(self, page_limit):
        self.page_limit = page_limit

    def _process_commits(self, df):
        commits = df['commit'].apply(pd.Series)
        commits.columns = ['commit_'+s for s in commits.columns]
        df = pd.concat([df.drop(['commit'], axis=1), commits], axis=1)

        date = df['commit_author'].apply(pd.Series)['date'].apply(pd.to_datetime)
        df = pd.concat([df, date], axis=1)

        login = df['author'].apply(pd.Series)['login']
        df = pd.concat([df, login], axis=1)

        # choose what to export
        df = df[['login', 'commit_message', 'date']]
        df.rename(columns={'commit_message': 'message'}, inplace=True)
        return df

    def _process_issues(self, df):
        return df

    def initial_download(self, endpoint):
        df = self._all_repos_endpoints(endpoint)
        df.reset_index(inplace=True)

        process_functions = {
            "commits": self._process_commits,
            "issues": self._process_issues
        }

        # processing df depending on endpoint
        df = process_functions[endpoint](df)

        # export to DB
        engine = create_engine(self.DB_URI)
        df.to_sql(name=endpoint, con=engine, index=False, if_exists="replace")
        return df

    def _incremental_single_repo(self, repo, endpoint):
        # first request - check if updated
        url = "https://api.github.com/repos/"+repo+self.endpoints[endpoint]
        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.USER, self.TOKEN),
            headers={'If-Modified-Since': self.last_modified[repo][endpoint]})

        if response.status_code != 304:
            df = self._single_repo_endpoints(repo, endpoint)

        return response

        # df = pd.DataFrame(response.json())
        # last_page, next_url, next_page_num, last_modified = self._parse_header(response)        





if __name__ == '__main__':
    app_config = {}
    app_config['GIT_REPOS'] = ['bitcoin/bitcoin']
    app_config['GIT_SECRET'] = {'USER': 'omdv', 'TOKEN': 'bdbae9884072bba932f755ee370fd85f001a2928'}
    app_config['SQLALCHEMY_DATABASE_URI'] = 'none'
    poller = GitPoller(app_config)
