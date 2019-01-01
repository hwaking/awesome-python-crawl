# encoding:utf-8

import urllib
import urllib.request
from lxml import etree
from tqdm import tqdm

from progressbar import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import Config

config = Config()
logger = config.logger

class Crawl(object):

    def __init__(self,url,title,date):
        self.url = url
        self.title = title
        self.date = date

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    def getUrl(self):
        try:
            req = urllib.request.Request(
                url=self.url, headers=self.headers
            )
            str_html = urllib.request.urlopen(req).read().decode('utf-8')
            html = etree.HTML(str_html)
            url = html.xpath("//ul[@class='zw_malei3']/li/span/a/@href")
            title = html.xpath("//ul[@class='zw_malei3']/li/span/a/@title")
            for url,title in zip(url,title):
                yield url,title
        except:
            yield self.url,self.title

    def pdf_download(self, url, title):
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
            logger.info('File {} already download !'.format(title))

    def download(self):
        count = 0
        status = False
        urllist = list(self.getUrl())
        if not urllist:
            status = True

        for pair in tqdm(urllist):
            try:
                url,title = pair
                self.pdf_download(url, title)
                count += 1
            except:
                logger.info('Download failed pair {}!!!'.format(str(pair)))
                status = True
        logger.info("Download {}篇 Now!".format(count))
        return count, status


def main(url,pagenum=1):
    """
    :param url: str, 抓取页面url
    :param pagenumber: int，从该页开始抓取，不指定则从头开始抓取
    :return: None
    """
    # chrome 模拟浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_driver = 'chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_driver,
                              chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    # 定位到“企业债”，并等待加载动态页面，加载时间设为3s
    driver.find_element_by_xpath("//span[@id='span_21280']").click()
    time.sleep(8)
    # 跳转到js固定框架（重要），并模拟跳转页面到指定开始抓取页面位置
    driver.switch_to.frame('ffrIframe')
    if pagenum > 1:
        path = '//select[@onchange="javascript:goPage(this.value)"]/option[@value="'+str(pagenum)+'"]'
        # print(path)
        driver.find_element_by_xpath(path).click()
        # driver.find_element_by_xpath('//select[@onchange="javascript:goPage(this.value)"]/option[@value="500"]').click()
    #等待页面跳转加载完成
    time.sleep(8)
    download_count = 0
    logger.info('**** Begin to Download Page {} Now! ****'.format(pagenum))
    while True:
        linknum=1
        for sel in driver.find_elements_by_xpath("//ul[@class='fx_news_list']/li"):
            date = sel.find_element_by_xpath("span[1]").text
            title = sel.find_element_by_xpath("span[2]/a").get_attribute("title")
            url = sel.find_element_by_xpath("span[2]/a").get_attribute("href")
            if url in config.urllib:
                logger.info('URL Files {} already download!!!'.format(title))
                continue

            logger.info('第-{}-条：title：{}'.format(linknum, title))
            count, status = Crawl(url,title,date).download()
            if status:
                # 说明该页未下载完成，故后续重复下载，直到下载完成为止
                continue
            config.save_to_urllib(url+'\n')
            download_count += count
            linknum += 1
        logger.info('>>> Finished crawl page {} now! Present total download {} pdfs!\n'.format(pagenum,download_count))
        time.sleep(8)
        try:
            driver.find_element_by_link_text('下一页>>').click()
            time.sleep(8)
        except:
            logger.info('>>> Finished Crawl on page {}, total crawled {} pdfs!'.format(pagenum, download_count))
            break
        pagenum += 1
        logger.info('**** Begin to Download Page {} Now! ****'.format(pagenum))
    driver.close
if __name__ == '__main__':
    url = 'http://www.chinabond.com.cn/Channel/21000'
    pagenum = int(sys.argv[-1])
    if pagenum < 1 or type(pagenum)!=int:
        raise ValueError(u'起始页数必须为大于1的整数')
    if pagenum:
        main(url, pagenum)
    else:
        main(url)
