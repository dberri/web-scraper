from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen
from pathlib import Path
import os
import time

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

    def __init__(self, directory, name, url):
        self.directory = directory
        self.name = name
        self.url = url

    def download(self):
        picFile = Path(self.directory+'/%s' % self.name)
        if picFile.is_file():
            print(self.name)
            print('File already exists...')
        else:
            txt = open(self.directory+'/%s' % self.name, "wb")
            req = Request(self.url, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
            try:
                theFile = urlopen(req).read()
            except Exception as e:
                print('Encoding error: ', e)
                return

            txt.write(theFile)
            txt.close()
            print(self.name)


class Spider(object):

    def __init__(self, url, link_class, img_class):
        self.url = url
        self.img_class = img_class
        self.link_class = link_class

    def create_folder(self, name):
        if not os.path.exists(name):
            print(bcolors.HEADER + 'FOLDER: ' + name + bcolors.ENDC)
            os.makedirs(name)
            return True
        else:
            print(bcolors.WARNING + 'FOLDER already exists...' + bcolors.ENDC)
            return False

    def get_img_links(self, url):
        driver.get(url)

        scroll_down()

        images = driver.find_elements(By.CLASS_NAME, self.img_class)
        print('Quantity of files: ', len(images))
        print('=' * 25)

        pics = {}
        img_links = []
        try:
            first_link = images[0].get_attribute('src')
            split_link = first_link.split('/')
            # directory = 'output/' + '-'.join(split_link[-1].split('-')[0:-1])
            directory = 'output/' + split_link[-1].split('.')[0]
            print(directory)

            for img in images:
                link  = img.get_attribute('src')
                img_links.append(link)

            pics[directory] = img_links
        except Exception as e:
            print(e)

        return pics

    def get_link_list(self, driver):
        link_parents = driver.find_elements(By.CLASS_NAME, self.link_class)

        list_links = []
        for link in link_parents:
            try:
                a = link.find_elements(By.TAG_NAME, 'a')
                href = a[0].get_attribute('href')
                list_links.append(href)
            except Exception as e:
                print(e)

        return list_links

    def create_pictures(self, pics):
        for directory in pics.keys():
            if self.create_folder(directory):
                for url in pics[directory]:
                    name = url.split('/')[-1]
                    pic = Picture(directory, name, url)
                    pic.download()



def start(url):
    for u in url:
        driver.get(u)

        scroll_down()

        # spider = Spider(u, img_class='size-full', link_class='post-thumbnail')
        spider = Spider(u, img_class='lazyimg', link_class='albumPhoto')
        list_links = spider.get_link_list(driver)

        for link in list_links:
            pics = spider.get_img_links(link)
            spider.create_pictures(pics)

def scroll_down():
    script = """
    window.scrollBy(0,10);
    """
    for _ in range(2000):
        driver.execute_script(script)
        time.sleep(0.001)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    login()
    
    driver.close()
