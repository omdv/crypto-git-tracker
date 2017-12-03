import requests
import re
import pandas as pd
from requests.auth import HTTPBasicAuth
from functools import reduce


class GitAPIWrapper():
    def __init__(self, repos, auth):
        self.repos = repos
        self.endpoints = {
            'commits': '/commits?per_page=100',
            'issues': '/issues?per_page=100'
        }
        self.USER = auth['USER']
        self.TOKEN = auth['TOKEN']

    def _parse_header(self, response):
        pages = response.headers['Link'].split(", ")
        next_page = [s for s in pages if 'rel="next"' in s]
        end = False
        if next_page:
            next_page_num = int(re.findall('&page=(\d+)', next_page[0])[0])
            next_url = re.findall('\<(\S+)\>', next_page[0])[0]
        else:
            end = True
        return (end, next_url, next_page_num)

    def _single_repo_endpoints(self, repo, endpoint):
        # first request
        url = "https://api.github.com/repos/"+repo+self.endpoints[endpoint]
        response = requests.get(url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
        df = pd.DataFrame(response.json())
        last_page, next_url, next_page_num = self._parse_header(response)

        while next_page_num < 3:
            response = requests.get(next_url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
            last_page, next_url, next_page_num = self._parse_header(response)
            df = pd.concat([df, pd.DataFrame(response.json())])
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

    def download_commits(self):
        df = self._all_repos_endpoints('commits')
        df.reset_index(inplace=True)

        commits = df['commit'].apply(pd.Series)
        commits.columns = ['commit_'+s for s in commits.columns]
        df = pd.concat([df.drop(['commit'], axis=1), commits], axis=1)

        date = df['commit_author'].apply(pd.Series)['date'].apply(pd.to_datetime)
        df = pd.concat([df, date], axis=1)

        return df

    def download_issues(self):
        df = self._all_repos_endpoints('issues')
        df.reset_index(inplace=True)

        return df


if __name__ == '__main__':
    git = GitAPIWrapper(['bitcoin/bitcoin'])
