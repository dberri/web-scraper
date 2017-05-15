# -*- coding: utf-8 -*-
import os
import urllib
import urllib.request
from urllib.request import Request, urlopen
import bs4 as bs
from pathlib import Path
import requests
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Picture(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def save(self, directory='output/'):

        picFile = Path(directory+'%s' % self.name)
        if picFile.is_file():
            print(self.name)
            print('File already exists...')
        else:
            txt = open(directory+'%s' % self.name, "wb")
            req = Request(self.url, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
            theFile = urlopen(req).read()
            txt.write(theFile)
            txt.close()
            print(self.name)


class Spider(object):

    def __init__(self, url, data):
        self.url = url
        self.soup = bs.BeautifulSoup(data.content, 'lxml')

    def try_link_in_anchor(parent):
        try:
            link = parent.a['href']
            return link

        except Exception as b:
            print('Erro a: ', b)

        else:
            return False

    def try_link_in_image(parent):
        try:
            link = parent.img['src']
            return link

        except Exception as e:
            print('Erro b: ', e)

        else:
            return False

    def get_img_links(self, tag, tag_class, parent_of_target=False):
        list_img = self.soup.find_all(tag, {'class': tag_class})
        print('Quantity of files: ', len(list_img))
        print('=' * 25)
        links_names = {}
        if parent_of_target:
            for parent in list_img:
                try:
                    img_link = parent.img['src']
                except Exception as e:
                    print(e)
                    img_link = parent.a['href']

                img_name = img_link.split('/')[-1]
                links_names[img_name] = img_link
        else:
            for img in list_img:
                img_link = img['src']
                img_name = img_link.split('/')[-1]
                links_names[img_name] = img_link

        return links_names



def main_spider(url, new_directory=False, tag='img', tag_class='', isParent=False):
    no_pages = len(url)

    print('=' * 25)

    for i in range(0, no_pages):
        data = requests.get(url[i], headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        webpage = Spider(url[i], data)
        links_dict = webpage.get_img_links(tag=tag, tag_class=tag_class, parent_of_target=isParent)

        if new_directory:
            # directory = 'output/' + list(links_dict.keys())[0].split('.')[0] + '/'
            directory = 'output/' + url[i].split('/')[-1] + '/'
            print(bcolors.HEADER + 'FOLDER: ' + directory + bcolors.ENDC)
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:
                print(bcolors.WARNING + 'FOLDER already exists...' + bcolors.ENDC)
                continue

        current = 0
        for name, link in links_dict.items():
            pic = Picture(name, link)
            if new_directory:
                pic.save(directory)
            else:
                pic.save()

            current += 1

        print('=' * 25)

if __name__ == '__main__':
    main_spider([''], tag='div', tag_class='')


# TODO
# Change directory
# check if there's a directory and save or not with the given directory
# check if there's a string in the link before saving the link then give messsage for exception
