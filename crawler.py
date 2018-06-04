import os

import requests
from bs4 import BeautifulSoup


def search_webtoon():
    file_path = 'data/webtoon_list.html'
    url = 'http://comic.naver.com/webtoon/weekday.nhn'

    if os.path.exists(file_path):
        html = open(file_path, 'rt').read()
    else:
        response = requests.get('http://comic.naver.com/webtoon/weekday.nhn')
        webhtml = response.text
        html = open(file_path, 'wt').write(webhtml)

    soup = BeautifulSoup(html, 'lxml')
    title = soup.select_one()

    while True:
        choice = input('안내) Ctrl+C로 종료합니다.\n'
                       '검색할 웹툰명을 입력해주세요: ')
        if choice == 1:
            print('1. universe\n 2. universe')


if __name__ == '__main__':
    search_webtoon()