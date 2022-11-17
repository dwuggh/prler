#!/usr/bin/env python3

import requests
import time
import random
from bs4 import BeautifulSoup

def get_soup(text):
    data = text.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    soup = BeautifulSoup(data, 'html.parser')
    return soup

class PRLBot(object):
    
    def __init__(self) -> None:
        self.session = requests.Session()
        self.ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        self.f = open("results.txt", "w")
        self.session.headers.update({
            'user-agent': self.ua
        })
        # self.session.headers
        self.toc_sections = [
            'all',
            'editorials-and-announcements',
            'general-physics-statistical-and-quantum-mechanics-quantum-information-etc',
            'gravitation-and-astrophysics',
            'elementary-particles-and-fields',
            'nuclear-physics',
            'atomic-molecular-and-optical-physics',
            'nonlinear-dynamics-fluid-dynamics-classical-optics-etc',
            'plasma-and-beam-physics',
            'condensed-matter-structure-etc',
            'condensed-matter-electronic-properties-etc',
            'polymer-soft-matter-biological-climate-and-interdisciplinary-physics',
            'comments',
            'errata'
            ]

    def fetch_toc_sections(self):
        url = "https://journals.aps.org/prl/recent"
        resp = self.session.get(url)
        soup = get_soup(resp.text)
        tocs = []
        for el in soup.find("div", {"data-name": "toc_section"}).find_all("input"):
            tocs.append(el['value'])

        return tocs


    def get_recent(self, page=1, toc_section=None):
        url = "https://journals.aps.org/prl/recent"
        api_url = "https://journals.aps.org/_api/v1/articles/"
        resp = self.session.get(url, params={
            "page": page,
            "toc_section[]": self.toc_sections if toc_section is None else toc_section,
            "article_type[]": ["letter"]
            })
        soup = get_soup(resp.text)
        search_result_list = soup.find_all(class_="article-result")
        last_year = ""
        for item in search_result_list:
            id = item['data-id']
            authors = item.find("h6", {"class": "authors"}).text
            pub_info = list(item.find("h6", {"class": "pub-info"}).strings)
            year = pub_info[-1]
            el = item.find("h5", {"class": "title"}).a
            title = "".join(el.strings)
            url = el['href']

            time.sleep(random.uniform(5., 7.))
            api_url_item = api_url + id + "/abstract"
            abstract = self.session.get(api_url_item, headers={"x-requested-with": "XMLHttpRequest"})
            date = time.strptime(year.split('Published')[-1].strip(), "%d %B %Y")
            abs_text = "".join(get_soup(abstract.text).strings)
            dmy = time.strftime("%d/%m/%Y", date)
            self.f.write(title)
            self.f.write("\n")
            self.f.write(authors)
            self.f.write("\n")
            self.f.write(abs_text)
            self.f.write("\n")
            self.f.write(dmy)
            self.f.write("\n\n\n")
            # last_year = year[-4:]

        return date.tm_year


if __name__ == '__main__':
    import sys
    bot = PRLBot()
    argv = sys.argv
    # toc_section=[
    #         'general-physics-statistical-and-quantum-mechanics-quantum-information-etc',
    #         'atomic-molecular-and-optical-physics',
    #         'nonlinear-dynamics-fluid-dynamics-classical-optics-etc',
    #         'condensed-matter-structure-etc',
    #         'condensed-matter-electronic-properties-etc',
    #     ]
    # range: 2 - 11
    toc_section = [bot.toc_sections[int(argv[1])], ]
    this_year = True
    page = 1
    while this_year:
        year = bot.get_recent(page, toc_section)
        page = page + 1
        if int(year) == 2016:
            this_year = False
            break
        time.sleep(random.uniform(4., 6.))
    bot.f.close()
    # bot.fetch_toc_sections()














