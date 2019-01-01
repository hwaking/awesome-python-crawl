# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from pybloom import BloomFilter
from hashlib import md5
from scrapy.mail import MailSender
import os
import json
import codecs


class GanjiPipeline(object):
    def __init__(self):
        #mail
        # self.mailer = MailSender.from_settings(settings)
        #mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION']+"_urllog"]
        #bloom file
        filename= settings['MONGODB_COLLECTION']+".blm"
        #pybloom
        num = (int(settings['CrawlCar_Num'])+self.collection.count())*1.1
        self.df = BloomFilter(capacity=num,error_rate=0.01)
        #read
        isexists = os.path.exists(filename)
        self.fa = open(filename, "a")
        if isexists:
            fr = open(filename, "r")
            lines = fr .readlines()
            for line in lines:
                line =line.strip('\n')
                self.df.add(line)
            fr.close()
        else:
            for i in self.collection.find():
                if "status" in i.keys():
                    item =i["status"]
                    item = md5(item).hexdigest()
                    self.df.add(item)
                    self.fa.writelines(item + '\n')
        #count
        self.counts=0
    def process_item(self, item, spider):
        valid = True
        i = md5(item['status']).hexdigest()
        returndf = self.df.add(i)
        if returndf:
            valid = False
        else:
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))
        if valid:
            self.fa.writelines(i + '\n')
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            print "scrapy                    " + str(self.counts) + "                  items \n"
        else:
            logging.log(msg="Car duplicated!", level=logging.INFO)
        #log save
        urlog = {'url': item['url'], 'grabtime': item['grabtime']}
        self.collectionurllog.insert(urlog)
        return item

    def close_spider(self, spider):
        self.connection.close()
        self.fa.close()
