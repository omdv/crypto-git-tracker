import requests
import re
import pandas as pd
import datetime as dt
from requests.auth import HTTPBasicAuth
from functools import reduce
from sqlalchemy import create_engine


class GitWatcher():
    def __init__(self, ticker, apihandle, repo, last_update):
        self.endpoint = '/commits?per_page=100'
        self.ticker = ticker
        self.apihandle = apihandle
        self.repo = repo
        self.last_update = last_update

    """
    Separate method to pass config after instantiation of Flask app
    """
    def set_app_config(self, app_config):
        self.USER = app_config['GIT_USER']
        self.TOKEN = app_config['GIT_TOKEN']
        self.DB_URI = app_config['SQLALCHEMY_DATABASE_URI']

    """
    Aux method to get the rate limit
    """
    def get_rate_limit(self):
        url = "https://api.github.com/rate_limit"
        response = requests.get(url, auth=HTTPBasicAuth(self.USER, self.TOKEN))
        return int(response.headers['X-RateLimit-Remaining'])

    def set_page_limit(self, page_limit):
        self.page_limit = page_limit

    def _datetime_from_string(self, last_update):
        return dt.datetime.strptime(last_update, "%a, %d %b %Y %H:%M:%S %Z")

    def _string_from_datetime(self, last_update):
        return last_update.strftime("%a, %d %b %Y %H:%M:%S") + ' GMT'

    def _iso_datetime(self, last_update):
        return last_update.strftime("%Y-%m-%dT%H:%M:%S") + 'GMT'

    """
    Parse response header.
    Older records are at higher pages
    Returns:
    - end: whether this is the last page
    - next_url: if there is a next_url
    - next_page_num
    - last_page_num
    """
    def _parse_header(self, response):
        # print out errors
        try:
            last_modified = response.headers['Last-Modified']
        except:
            print(response.content)
            print(response.headers)
            print(response.request)
            print(response.url)
            last_modified = -1
            pass

        # if less than 100 items there is no 'Link' in response headers
        if 'Link' in response.headers:
            pages = response.headers['Link'].split(", ")
            next_page = [s for s in pages if 'rel="next"' in s]
            last_page = [s for s in pages if 'rel="last"' in s]
            prev_page = [s for s in pages if 'rel="prev"' in s]
            end = False

            if last_page:
                last_page_num = int(re.findall('&page=(\d+)', last_page[0])[0])
            else:
                last_page_num =\
                    int(re.findall('&page=(\d+)', prev_page[0])[0])+1

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

    def _download_page(self, pagenum):
        url = "https://api.github.com/repos/" + self.repo + self.endpoint
        url = url + '&page={}'.format(pagenum)
        url = url + '&since={}'.format(self._iso_datetime(self.last_update))

        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.USER, self.TOKEN))

        return pd.DataFrame(response.json()), response

    def _process_commits(self, df):
        commits = df['commit'].apply(pd.Series)
        commits.columns = ['commit_' + s for s in commits.columns]
        df = pd.concat([df.drop(['commit'], axis=1), commits], axis=1)

        date = df['commit_author'].apply(pd.Series)['date'].\
            apply(pd.to_datetime)
        df = pd.concat([df, date], axis=1)

        login = df['author'].apply(pd.Series)['login']
        df = pd.concat([df, login], axis=1)

        # choose what to export
        df = df[['login', 'commit_message', 'date', 'repo', 'ticker',
                 'apihandle', 'url']]
        df.rename(columns={'commit_message': 'message'}, inplace=True)

        return df

    def download(self):
        url = "https://api.github.com/repos/" + self.repo + self.endpoint
        url = url + '&since={}'.format(self._iso_datetime(self.last_update))

        # first request
        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.USER, self.TOKEN),
            headers={'If-Modified-Since':
                     self._string_from_datetime(self.last_update)})

        if response.status_code != 304:
            response_dataframes = []

            # download last page
            _, _, _, _, last_page_num =\
                self._parse_header(response)

            while last_page_num > 0:
                df, response = self._download_page(last_page_num)
                response_dataframes.append(df)
                _, _, _, last_modified, _ = self._parse_header(response)
                last_page_num -= 1

            # prepare the dataframe
            df = reduce(lambda x, y: pd.concat([x, y]), response_dataframes)
            df.reset_index(inplace=True)
            df['repo'] = self.repo
            df['ticker'] = self.ticker
            df['apihandle'] = self.apihandle
            df = self._process_commits(df)

            # export to DB
            engine = create_engine(self.DB_URI)
            df.to_sql(name='commits', con=engine, index=False,
                      if_exists="append")

        else:
            last_modified = None

        return last_modified


if __name__ == '__main__':
    app_config = {}
    app_config['GIT_USER'] = 'omdv'
    app_config['GIT_TOKEN'] = 'bdbae9884072bba932f755ee370fd85f001a2928'
    app_config['SQLALCHEMY_DATABASE_URI'] =\
        'postgres://postgres:postgres@localhost:5435/analytics_dev'

    engine = create_engine(app_config['SQLALCHEMY_DATABASE_URI'])
    repos = pd.read_sql('control_repos', engine)

    for _r in repos.values:
        watcher = GitWatcher(_r[1], _r[2], _r[3], _r[4])
        watcher.set_app_config(app_config)
        new_date = watcher.download()
