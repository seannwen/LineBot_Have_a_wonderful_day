# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def browse(articles_info, bs4_html):
    # Find articles
    articles = bs4_html.find_all("div", {"class": "r-ent"})
    for article in articles:
        push_number = article.find("div", {"class": "nrec"})
        title = article.find("div", {"class": "title"}).find('a')

        # Delete deleted articles and display pushes(display 0 if there is no push)
        if title:
            if push_number.text:
                articles_info.append('[{}] https://www.ptt.cc{} {}'.format(push_number.text, title.get('href'), title.text))
            else:
                articles_info.append('[{}] https://www.ptt.cc{} {}'.format('0', title.get('href'), title.text))
    return articles_info


# Find hotboards
def find_hotboards():
    bs4_html = get_bs4_html('https://www.ptt.cc/bbs/hotboards.html')
    hotboards = set()
    boardnames = bs4_html.find_all("div", {"class": "board-name"})
    hotboards = [boardname.text.lower() for boardname in boardnames]
    return hotboards


# Get the content after bs4
def get_bs4_html(url):
    # Sending request to the website
    res = requests.get(url)
    html_doc = res.text
    bs4_html = BeautifulSoup(html_doc, "html.parser")
    return bs4_html


def find_next_page(bs4_html):
    older_page = None
    # Get the url for the next page
    find_next_page = bs4_html.find_all('a', {"class": "btn wide"})
    for next_page in find_next_page:
        if next_page.text == "‹ 上頁":
            older_page = 'https://www.ptt.cc{}'.format(next_page.get('href'))
            print(older_page)

    # If not next page, print error message
    if not older_page:
        return None
    return older_page


if __name__ == '__main__':
    print(find_hotboards())
