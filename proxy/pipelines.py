# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from proxy.items import ProxyItem,ArticleItem

from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql,5,host='127.0.0.1',user='root',passwd='King00cui',db='spider',port=3306)

# class ProxyPipeline(object):
#     def process_item(self, item, spider):
#         print("pipline",item)
#         return item
#
# class MySQLPipline(object):
#     def process_item(self,item,spider):
#         print("mysql pipline:",item)
#         # values = (
#         #     item['ip'],
#         # )
#
#         # sql = 'insert into remote_host(ip) values (%s)'
#         #
#         # conn = pool.connection()
#         # cur = conn.cursor()
#         # cur.execute(sql,values)
#         # conn.commit()
#         # cur.close()
#         # conn.close()
#
#         return item


class MySQLPipeline(object):
    def process_item(self, item, spider):
        print("mysql pipline:", item)

        if isinstance(item, ProxyItem):
            values = (
                item['ip'],
            )
            sql = 'INSERT INTO remote_host(ip) VALUES (%s)'
            self.insert(sql, values)

        elif isinstance(item, ArticleItem):
            values = (
                item["title"],
                item["url"],
                item["img"],
                item["content"]
            )
            sql = 'INSERT INTO article(title, url, img, content) VALUES (%s, %s, %s, %s)'
            self.insert(sql, values)

    @staticmethod
    def insert(sql, values):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()


class ProxyPipeline(object):
    def process_item(self, item, spider):
        print("pipline:", item)
        return item

