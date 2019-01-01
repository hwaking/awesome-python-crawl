# -*- coding: utf-8 -*-
import scrapy
from car_sohu.items import SohunewcarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re

website ='sohunewcar'

class CarSpider(scrapy.Spider):

    name = website
    # allowed_domains = ["http://db.auto.sohu.com/"]
    # start_urls = [
    #     "http://db.auto.sohu.com"
    # ]
    def __init__(self):
        # problem report
        # self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 50000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        #global carnum
        fl = open("D:\spiderdata\sohunewcar.txt", 'r')
        lines = fl.read()
        lines = lines.replace('var TbrandMods = ', "").replace(";", "").strip()
        jsdata = json.loads(lines)
        cars=[]
        for i in jsdata[0]:
            for j in jsdata[0][i]:
                if j.has_key('list'):
                    line = j['list']
                for k in line:
                    if k.has_key('s'):
                        str = k['s']
                    for m in str:
                        brandname = m['n']
                        brandid = m['d']
                        if m.has_key('b'):
                            str1 = m['b']
                        for ck in str1:
                            familyname = ck['n']
                            familyid = ck['d']
                            urlbase="http://db.auto.sohu.com/api/para/data/model_"+familyid+".json"
                            metadata={'brandid':brandid,'brandname':brandname,'familyid':familyid,'familyname':familyname}
                            car=scrapy.Request(urlbase,meta={'metadata': metadata})
                            cars.append(car)
        return cars


    # brand select
    def parse(self, response):
        metadata = response.meta['metadata']
        if response.body.find('{')!=-1:
            mdata=json.loads(response.body_as_unicode().replace("%u","\\u").replace("%","\u00"))
            if mdata.has_key('SIP_M_TRIMS'):
                for line in mdata['SIP_M_TRIMS']:
                    trimid=line['SIP_T_ID']
                    trimname=line['SIP_T_NAME']
                    trimgear=line['SIP_T_GEAR']
                    trimdisp=line['SIP_T_DISP']
                    trimyear=line['SIP_T_YEAR']
                    trimdata=dict({'trimid':trimid,'trimname':trimname,'trimgear':trimgear,'trimdisp':trimdisp,'trimyear':trimyear},**metadata)
                    urlbase="http://db.auto.sohu.com/api/para/data/trim_"+str(trimid)+".json"
                    yield scrapy.Request(urlbase,meta={'metadata': trimdata}, callback=self.trim_parse)

    def trim_parse(self,response):
        item=SohunewcarItem()
        tmdata = json.loads(response.body_as_unicode().replace("%u","\\u").replace("%","\u00"))
        metadata = response.meta['metadata']
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['url']=response.url
        if metadata:
            item['brandid']=metadata['brandid']
            item['brandname']=metadata['brandname']
            item['familyid']=metadata['familyid']
            item['familyname']=metadata['familyname']
            item['trimid']=metadata['trimid']
            item['trimname']=metadata['trimname']
            item['trimgear']=metadata['trimgear']
            item['trimdisp']=metadata['trimdisp']
            item['trimyear']=metadata['trimyear']
        # print metadata
        # def namelist_parse(self,response):
        #     yield  scrapy.Request("http://db.auto.sohu.com/yiqiaudi/4207/trim.html",callback=self.namelist_parse)
        #     for line in response.xpath('//table[@id="trimArglist"]/t')

        namelist={u"厂商指导价":"SIP_C_102",u"4S店最低报价":"SIP_C_103",u"车厂":"SIP_C_104",u"级别":"SIP_C_105",
                  u"车体结构":"SIP_C_106",u"长x宽x高(mm)":"SIP_C_293",u"发动机":"SIP_C_107",u"变速箱":"SIP_C_108",
                  u"动力类型":"SIP_C_303",u"官方最高车速(km/h)":"SIP_C_112",u"工信部油耗(L/100km)":"SIP_C_294",
                  u"官方0-100加速(s)":"SIP_C_113",u"保养周期":"SIP_C_114",u"保养费用":"SIP_C_304",u"保修政策":"SIP_C_115",
                  u"碰撞星级":"SIP_C_116",u"更多实测参数":"SIP_C_295",u"长度(mm)":"SIP_C_117",u"宽度(mm)":"IP_C_118",
                  u"高度(mm)":"SIP_C_119",u"轴距(mm)":"SIP_C_120",u"前轮距(mm)":"SIP_C_121",u"后轮距(mm)":"SIP_C_122",
                  u"整备质量(kg)":"SIP_C_123",u"车身结构":"SIP_C_124",u"车门数(个)":"SIP_C_125",u"座位数(个)":"SIP_C_126",
                  u"油箱容积(L)":"SIP_C_127",u"行李厢容积(L)":"SIP_C_128",u"最小离地间隙(mm)":"SIP_C_129",
                  u"最小转弯半径(m)":"SIP_C_130",u"接近角":"SIP_C_131",u"离去角":"SIP_C_132",u"发动机描述":"SIP_C_134",
                  u"发动机型号":"SIP_C_135",u"排量(L)":"SIP_C_136",u"汽缸容积(cc)":"SIP_C_137",u"工作方式":"SIP_C_138",
                  u"汽缸数(个)":"SIP_C_139",u"汽缸排列形式":"SIP_C_140",u"每缸气门数(个)":"SIP_C_141",u"气门结构":"SIP_C_142",
                  u"压缩比":"SIP_C_143",u"最大马力(ps)":"SIP_C_297",u"最大功率(kW/rpm)":"SIP_C_298",
                  u"最大扭矩(N·m/rpm)":"SIP_C_299",u"升功率(kW/l)":"SIP_C_148",u"混合类型":"SIP_C_305",u"插电形式":"SIP_C_306",
                  u"电动机最大功率(kW)":"SIP_C_307",u"电动机最大扭矩":"SIP_C_308",u"最大行驶里程(km)":"SIP_C_309",
                  u"电池种类":"SIP_C_310",u"电池容量(kWh)":"SIP_C_311",u"燃料":"SIP_C_149",u"供油方式":"SIP_C_150",
                  u"缸盖材料":"SIP_C_151",u"缸体材料":"SIP_C_152",u"排放标准":"SIP_C_155",u"变速箱简称":"SIP_C_156",
                  u"挡位个数":"SIP_C_157",u"变速箱类型":"SIP_C_158",u"电动机最大功率(kW)":"SIP_C_307",u"电动机最大扭矩":"SIP_C_308",
                  u"最大行驶里程(km)":"SIP_C_309",u"电池种类":"IP_C_310",u"电池容量(kWh)":"SIP_C_311",u"电机数":"SIP_C_353",
                  u"驱动方式":"SIP_C_159",u"前悬挂类型":"SIP_C_160",u"后悬挂类型":"SIP_C_161",u"底盘结构":"SIP_C_162",
                  u"前轮胎规格":"SIP_C_163",u"后轮胎规格":"SIP_C_164",u"前制动器类型":"SIP_C_167",u"后制动器类型":"SIP_C_168",
                  u"主/副驾驶座安全气囊":"SIP_C_177_178",u"前/后排侧气囊":"SIP_C_179_180",u"自动防抱死(ABS等)":"SIP_C_185",
                  u"制动力分配":"SIP_C_186",u"刹车辅助":"SIP_C_187",u"牵引力控制":"SIP_C_188",u"车身稳定控制":"SIP_C_189",
                  u"天窗型式":"SIP_C_316",u"前/后倒车雷达":"SIP_C_343_201",u"车身可选颜色":"IP_C_291",u"内饰可选颜色":"SIP_C_292",
                  u"近光灯":"SIP_C_318",u"远光灯":"SIP_C_347",u"日间行车灯":"SIP_C_260",u"前感应雨刷":"SIP_C_272",u"空调":"SIP_C_320"
                  }
        if tmdata:
            ptdata=dict()
            for line in namelist:
                value=namelist[line]
                if tmdata.has_key(value):
                    ptdata[line]=tmdata[value]
            itemnew = SohunewcarItem()
            itemnew = dict(item, **ptdata)
            yield itemnew
        else:
            yield item

