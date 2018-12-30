# -*- coding: utf-8 -*-
import scrapy
from webScrapy.items import WebscrapyItem
from webScrapy.items import actorItem
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
import string
from fontTools.ttLib import TTFont
import requests
import re
import os

'''
regex_woff = re.compile("(?<=url\(').*\.woff(?='\))")
regex_font = re.compile('(?<=&#x).{4}(?=;)')

def get_fontnumber(newfont, text):
    ms = regex_font.findall(text)
    for m in ms:
        text = text.replace(f'&#x{m};', get_num(newfont, f'uni{m.upper()}'))
    return text


def get_num(newfont, name):
    uni = newfont['glyf'][name]
    for k, v in fontdict.items():
        if uni == basefont['glyf'][k]:
            return v


def downloads(url, localfn):
    with open(localfn, 'wb') as sw:
        sw.write(requests.get(url).content)


basefont = TTFont('fonts\\base.woff')
fontdict = {'uniE36D': '0', 'uniF4D4': '8', 'uniF613': '9', 'uniF031': '2', 'uniE4B7': '6',
            'uniF26F': '3', 'uniF5BE': '1', 'uniF1B0': '4', 'uniE161': '5', 'uniE6D9': '7'}
'''

'''
class MaoyanSpiderSpider(scrapy.Spider):
    name = 'maoyan_spider'
    allowed_domains = ['maoyan.com']

    #分别是2015、2016、2017、2018年电影详细界面的url后缀
    yearld_list = ['&yearld=10','&yearld=11','&yearld=12','&yearld=13']
    start_urls = ['http://maoyan.com/films?showType=3&yearld=10']

    #解析response
    def parse(self, response):
        yearld_list = ['&yearld=10', '&yearld=11', '&yearld=12', '&yearld=13']
        for yearld in yearld_list:
            yield scrapy.Request('http://maoyan.com/films?showType=3'+yearld,callback=self.list_parse)


    def list_parse(self, response):
        house_detail_urls = response.xpath('//*[@id="app"]/div/div[2]/div/dl/dd/div/a/@href').extract()
        for house_detail_url in house_detail_urls:
            if house_detail_url:
                yield scrapy.Request('http://maoyan.com'+house_detail_url,callback=self.movie_detail_parse)
                pass

        next_url = response.xpath('//*[@id="app"]/div/div[2]/div[3]/ul/li[a="下一页"]/a/@href').extract()
        if next_url:
            next_url = next_url[0]
            yield scrapy.Request('http://maoyan.com/films'+next_url,callback=self.list_parse)



    def movie_detail_parse(self,response):
        #所需要的信息分散在movie信息界面的三个布局
        movie_page_layout1 = response.xpath('/html/body/div[3]/div/div[2]/div[1]')
        movie_page_layout2 = response.xpath('/html/body/div[3]/div/div[2]/div[3]')
        #movie_page_layout3

        #下载字体文件
        linkitem = response.xpath('/html/head/style/text()').extract()[0]
        woff = regex_woff.search(linkitem).group()
        wofflink = 'http:' + woff
        localname = 'fonts\\' + os.path.basename(wofflink)
        if not os.path.exists(localname):
            downloads(wofflink,localname)
        font = TTFont(localname)

        movie_item = WebscrapyItem()
        #其中含有unicode字符，beautifulsoup无法正常显示，只能用原始文本通过正则获取
        ms = movie_page_layout2.xpath('./div[1]/div/span').extract()[0]
        print(ms);
        movie_item['movie_score'] = get_fontnumber(font,ms)
        #print(movie_item['movie_score'])

        movieid = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div/@data-val').extract()[0].split('}')[0].split(':')[1]
        movie_item['movie_url_index'] = movieid
        movie_item['movie_name_chi'] = movie_page_layout1.xpath('./h3/text()').extract()[0]
        movie_item['movie_type'] = movie_page_layout1.xpath('./ul/li[1]/text()').extract()[0]
        #make_in and timelength mix
        #movie_item['make_in'] = movie_page_layout1.xpath('')
        movie_item['movie_releaseDate'] = movie_page_layout1.xpath('./ul/li[3]/text()').extract()[0]

        movie_item['movie_score'] = movie_page_layout2.xpath('./div[1]/div/span/span/text()').extract()[0]
        movie_item['movie_boxOffice'] = movie_page_layout2.xpath('./div[2]/div/span[1]/text()').extract()[0]


        movie_item['movie_directors'] = response.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li/div/a/text()')

'''

class MaoyanSpiderSpider(scrapy.Spider):
    name = 'maoyan_spider'
    allowed_domains = ['piaofang.maoyan.com']
    start_urls = ['http://piaofang.maoyan.com/rankings/year']

    count = 0

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:/Users/48093/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        self.browser.set_page_load_timeout(30)#30s后无反应刷新

    def closed(self,spider):
        print("spider close")
        self.browser.close()#关闭浏览器

    # 解析response
    def parse(self, response):
        house_detail_urls = []
        listNo = [3,4,2,5]
        for i in listNo:
            self.browser.find_element_by_xpath('//*[@id="tab-year"]/ul/li['+str(i)+']').click()
            time.sleep(3)
            #print(self.browser.page_source)
            house_detail_urls.append(re.compile(r"hrefTo,href:'/movie/.*?'").findall(self.browser.page_source))
            #print(house_detail_urls[0])
            #for house_detail_url in house_detail_urls[1]:
               # house_detail_url = house_detail_url.strip("hrefTo,href:''")
              #  if house_detail_url:
                #    self.count = self.count + 1
                    #print(self.count)
                    #yield scrapy.Request('http://piaofang.maoyan.com'+house_detail_url,callback=self.movie_detail_parse)
            print('finished--'+str(i))
            print(house_detail_urls)
        for house_detail_url in house_detail_urls:
            for detail_url in house_detail_url:
                detail_url = detail_url.strip("hrefTo,href:''")
                if detail_url:
                    self.count = self.count + 1
                    print(self.count)
                    yield scrapy.Request('http://piaofang.maoyan.com' + detail_url, callback=self.movie_detail_parse)


    def movie_detail_parse(self,response):

        movie_item = WebscrapyItem()

        movie_name_chi = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/p/span/text()').extract()
        if movie_name_chi:
            movie_item['movie_name_chi'] = movie_name_chi[0]
        #movie_item['movie_name_chi'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/p/span/text()').extract()[0]


        movie_name_eng =  response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/p/span/text()').extract()
        if movie_name_eng:
            movie_item['movie_name_eng'] = movie_name_eng[0]
        #movie_item['movie_name_eng'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/p/span/text()').extract()[0]


        movie_url_index = re.compile('/movie/.*?/boxshow').findall(response.text)
        if movie_url_index:
            movie_item['movie_url_index'] = movie_url_index[0].strip("/movieboxshow")
        #movie_item['movie_url_index'] = re.compile('/movie/.*?/boxshow').findall(response.text)[0].strip("/movieboxshow")
        #response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[2]/a/@href').extract()[0].strip('/movieaudienceRating?usePageCache=true')


        movie_score = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[2]/a/div[2]/div[2]/div/span[1]/text()').extract()
        if movie_score:
            movie_item['movie_score'] = movie_score[0]
        #movie_item['movie_score'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[2]/a/div[2]/div[2]/div/span[1]/text()').extract()[0]


        movie_item['movie_directors'] = response.xpath('/html/body/div[2]/section[2]/div/div/div[1]/div[1]/div[1]/div[2]/a/div/p/text()').extract()
        movie_item['movie_directors'] = '/'.join(movie_item['movie_directors'])
        movie_item['movie_stars'] = response.xpath('/html/body/div[2]/section[2]/div/div/div[1]/div[1]/div[2]/div[2]/a/div/p[1]/text()').extract()
        movie_item['movie_stars'] = '/'.join(movie_item['movie_stars'])


        movie_type = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/p/text()').extract()
        if movie_type:
            movie_item['movie_type'] = movie_type[0].strip().replace("\n",'')
        #movie_item['movie_type'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/p/text()').extract()[0].strip().replace("\n",'')


        make_in = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/p/text()').extract()
        if make_in:
            movie_item['make_in'] = make_in[0].strip().replace("\n",'').strip('/').strip()
        #movie_item['make_in'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/p/text()').extract()[0].strip().replace("\n",'').strip('/').strip()


        movie_boxOffice = response.xpath('/html/body/div[2]/section[1]/div/div[3]/a/div/div[3]/div[1]/p[2]/span[1]/text()').extract()
        if movie_boxOffice:
            movie_item['movie_boxOffice'] = movie_boxOffice[0]
        #movie_item['movie_boxOffice'] = response.xpath('/html/body/div[2]/section[1]/div/div[3]/a/div/div[3]/div[1]/p[2]/span[1]/text()').extract()[0]

        movie_boxOffice_unit = response.xpath('/html/body/div[2]/section[1]/div/div[3]/a/div/div[3]/div[1]/p[2]/span[2]/text()').extract()
        if movie_boxOffice_unit:
            movie_item['movie_boxOffice_unit'] = movie_boxOffice_unit[0]


        movie_timeLength = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/p/span/text()').extract()
        if movie_timeLength:
            movie_item['movie_timeLength'] = movie_timeLength[0]
        #movie_item['movie_timeLength'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/p/span/text()').extract()[0]


        movie_release = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[2]/a/span/text()').extract()
        if movie_release:
            movie_item['movie_releaseDate'] =movie_release[0]
        #movie_item['movie_releaseDate'] = response.xpath('/html/body/div[2]/section[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div[2]/a/span/text()').extract()[0]
        yield movie_item
        '''
        stars_list = response.xpath('/html/body/div[2]/section[2]/div/div/div[1]/div[1]/div[2]/div[2]/a/@href').extract()
        for star in stars_list:
            print(star)
            #yield scrapy.Request('http://piaofang.maoyan.com' + star, callback=self.actor_detail_parse)
        '''
        pass


    def actor_detail_parse(self,response):
        actor_item = actorItem()
        indexDict = response.xpath('//*[@id="pageData"]/text()').extract()[0].strip(" \n")
        indexDict = eval(indexDict)
        actor_item['actorIndex'] = indexDict['celebrityId']
        actor_item['actorName'] = indexDict['cnName']
        #nannv = response.xpath('/html/body/div[@class="sticky-container"]/div[@class="scroller cat-wrapper"]/div/div[@class="celeAnchor-container body-container"]').extract()[0]

        sex = re.compile('<span.*?[男女]</span>').findall(response.text)
        if sex:
            sex = sex[0].strip('</span>')
        actor_item['actorSex'] = sex
        yield actor_item
        pass


'''
     def parse(self, response):
        if response.xpath('//*[@id="tab-year"]/ul/li[@class = "active"]/text()').extract()[0] == '全部':
            print('aaaaaaaaaaaaaaaaaaaaaa')
            self.browser.find_element_by_xpath('//*[@id="tab-year"]/ul/li[2]').click()
            time.sleep(2)
            a = response
            print(self.browser.page_source)
            a.text = str(self.browser.page_source)
            self.list_parse(response = a)
'''