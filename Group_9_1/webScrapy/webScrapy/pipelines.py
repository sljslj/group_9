# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from webScrapy.items import WebscrapyItem,actorItem
from scrapy.exporters import CsvItemExporter
from webScrapy.spiders.itemCsvExporter import itemCsvExporter
import csv

class WebscrapyPipeline(object):
    def __init__(self):
        self.file1 = open('movie_data.csv','wb')
        self.file2 = open('actor_data.csv','wb')
        self.exporter1 = itemCsvExporter(self.file1,encoding="utf-8")
        self.exporter2 = CsvItemExporter(self.file2,encoding="utf-8")
        self.exporter1.start_exporting()
        self.exporter2.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item,WebscrapyItem):
            self.exporter1.export_item(item)
        elif isinstance(item,actorItem):
            self.exporter2.export_item(item)
        else:
            pass
        return item


    def close_spider(self,spider):
        self.exporter1.finish_exporting()
        self.exporter2.finish_exporting()
        self.file1.close()
        self.file2.close()