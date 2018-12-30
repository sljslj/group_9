# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #电影中文名
    movie_name_chi = scrapy.Field()
    #电影英文名
    movie_name_eng = scrapy.Field()
    #电影索引号
    movie_url_index = scrapy.Field()
    #评分
    movie_score = scrapy.Field()
    #导演
    movie_directors = scrapy.Field()
    #主演
    movie_stars = scrapy.Field()
    #类型
    movie_type = scrapy.Field()
    #出品国家
    make_in = scrapy.Field()
    #票房
    movie_boxOffice = scrapy.Field()
    #电影时长
    movie_timeLength = scrapy.Field()
    #上映时间
    movie_releaseDate = scrapy.Field()
    #票房单位
    movie_boxOffice_unit = scrapy.Field()


class actorItem(scrapy.Item):
    #演员姓名
    actorName = scrapy.Field()
    #演员性别
    actorSex = scrapy.Field()
    #演员索引
    actorIndex = scrapy.Field()

