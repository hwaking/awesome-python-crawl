#!/usr/bin/python
#encoding:utf-8


import time
import urllib
import os
import re
import urllib.request
from lxml import etree
import codecs

from progressbar import *
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawl(object):

    def __init__(self,url,title,date):
        self.url = url
        self.title = title
        self.date = date

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    def getUrl(self):
        try:
            req = urllib.request.Request(
                url=self.url,headers=self.headers
            )
            str_html = urllib.request.urlopen(req).read().decode('utf-8')
            html = etree.HTML(str_html)
            # print('html',html)
            url = html.xpath("//ul[@class='zw_malei3']/li/span/a/@href")
            title = html.xpath("//ul[@class='zw_malei3']/li/span/a/@title")
            for url,title in zip(url,title):
                yield url,title
        except:
            yield self.url,self.title

    def pdf_download(self,url,title):
        path = 'download/'+self.title
        if not os.path.exists(path):
            os.makedirs(path)
        req = urllib.request.Request(url=url, headers=self.headers)
        u = urllib.request.urlopen(req)
        outpath = os.path.join(path,title)
        if not os.path.exists(outpath):
            with open(outpath, 'wb') as out_f:
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    out_f.write(buffer)
        else:
            #print('File {} already download!!!'.format(title))
            pass

    def download(self):

        count = 0
        urllist = list(self.getUrl())
        from tqdm import tqdm
        for pair in tqdm(urllist):
            try:
                url,title = pair
                self.pdf_download(url, title)
                count+=1
                # print("Sucessful download 第{}篇".format(count))
            except:
                print('Download Error pair {}!!!'.format(pair))
        print("Download {}篇 Now!".format(count))
        return count


def logfile(save=True, data=''):
    outpath='./log/logfile.txt'
    if not os.path.exists(outpath):
        os.mkdir('log')
        f = open(os.path.join('log','logfile.txt'), 'w')
        f.close()

    model='r'
    if save:
        model='a+'
    with codecs.open(outpath, model, 'utf8') as log_f:
        if model=='a+':
            print('Download {} Successed!!\n'.format(data))
            log_f.write(data+'\n')
        else:
            data = [url.strip() for url in log_f.read().strip().split('\n')]
            return data

def main(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_driver = 'C://Users//hogen//Desktop//chromedriver'
    chrome_driver = 'chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_driver,
                              chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_xpath("//span[@id='span_21280']").click()
    time.sleep(3)
    driver.switch_to.frame('ffrIframe')
    time.sleep(2)
    pagenum,download_count = 1,0
    print('Begin downloading Now!!!')
    while True:
        linknum=1
        for sel in driver.find_elements_by_xpath("//ul[@class='fx_news_list']/li"):
            date = sel.find_element_by_xpath("span[1]").text
            title = sel.find_element_by_xpath("span[2]/a").get_attribute("title")
            url = sel.find_element_by_xpath("span[2]/a").get_attribute("href")

            urldatalib=logfile(save=False)
            if url in urldatalib:
                print('File {} already download!!!'.format(title))
                continue

            print('第-{}-条：title：{}'.format(linknum, title))
            count = Crawl(url,title,date).download()
            logfile(save=True,data=url)
            download_count += count
            linknum += 1
        print('>>> Finished crawl page {} now! Present total download {} pdfs!\n'.format(pagenum,download_count))
        try:
            time.sleep(3)
            driver.find_element_by_link_text('下一页>>').click()
            time.sleep(5)
        except:
            print('>>> Finished Crawl on page {}, total crawled {} pdfs!'.format(pagenum,download_count))
            break
        pagenum += 1
        print('**** Begin to Download Page {} Now! ****'.format(pagenum))
    driver.close()

if __name__ == '__main__':
    url = 'http://www.chinabond.com.cn/Channel/21000'
    main(url)

