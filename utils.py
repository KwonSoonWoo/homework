import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''

    def _get_info(self, attr_name):
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    @property
    def html(self):
        if not self._html:
            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }

            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_episode_list, params)
                html = response.text
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self._html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        soup = BeautifulSoup(self._html, 'lxml')

        table = soup.select_one('table.viewList')
        tr_list = table.select('tr')
        episode_list = list()
        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue

                url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
                url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
                query_string = parse.urlsplit(url_detail).query
                query_dict = parse.parse_qs(query_string)
                no = query_dict['no'][0]

                title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
                rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
                created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

                new_episode = Episode(
                    webtoon_id=self.webtoon_id,
                    no=no,
                    url_thumbnail=url_thumbnail,
                    title=title,
                    rating=rating,
                    created_date=created_date,
                )
                episode_list.append(new_episode)
            self._episode_list = episode_list

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    def webtoon(self):
        # 무슨 기능의 함수인지를 모르겠음.


    def crawl_title(self):
        # 요일별 전체 웹툰의 타이틀 정보를 리턴한다
        soup = BeautifulSoup(Webtoon.html, 'lxml')
        table = soup.select_one('div.list_area daily_all')
        title_list = table.select('div.col_inner')
        episode_list = list()
        for index, col in enumerate(title_list):
            return col

            title = soup.select_one(a.title)


    # episode_url을 리턴해주는 함수
    def url(self):
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        # webtoon_id 대신 Webtoon인스턴스를 받도록 함
        params = {
            'titleId': Webtoon.webtoon_id,
            'no': self.no,
        }
        episode_url = url + parse.urlencode(params)
        return episode_url

class EpisodeImage:
    def episode(self):
        pass

    def url(self):
        pass

    def file_path(self):
        pass


if __name__ == '__main__':
    pass