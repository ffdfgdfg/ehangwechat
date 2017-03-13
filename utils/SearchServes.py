# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from utils import BaseMsg
from utils import DataBase

class Serves(BaseMsg.MsgBase):
    def __init__(self):
        # 搜索对象的方法
        # 存储schema信息至'indexdir'目录下
        self.indexdir = 'indexdir/'

    def result(self, results):
        result_data = {
            'title': results['title'],
            'description': results['description'],
            'image': results['image'],
            'url': results['url']
        }
        return result_data
    def search(self, key):
        # 创建一个检索器
        ix = open_dir(self.indexdir)
        searcher = ix.searcher()
        # 检索标题中出现'文档'的文档
        results_title = searcher.find("title", u'%s' % (key))
        results_description = searcher.find("description", u'%s' % (key))

        # 数据格式为dict{'title':.., 'content':...}
        firstdoc = []
        if len(results_title) != 0:#返回的是结果列表，列表里包含字典，需要访问才行
            firstdoc.append(self.result(results_title[0]))
        elif len((results_description)) != 0:
            firstdoc.append(self.result(results_description[0]))
        else:
            firstdoc = None
        return firstdoc
    def AddIndex(self, DictItem):
        #添加检索列表
        if not os.path.exists(self.indexdir):
            os.mkdir(self.indexdir)
            # 使用结巴中文分词
            analyzer = ChineseAnalyzer()
            # 创建schema, stored为True表示能够被检索
            schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                            description=TEXT(stored=True, analyzer=analyzer),
                            image=TEXT(stored=True),
                            url=TEXT(stored=True))
            # 按照schema定义信息，增加需要建立索引的文档
            # 注意：字符串格式需要为unicode格式
            db=DataBase.MongoUtil()
            db.update('oplog', 'name', name='main', materialcount=0)
            ix = create_in(self.indexdir, schema)
        else:
            ix = open_dir(self.indexdir)
        writer = ix.writer()
        writer.add_document(title=u'%s' % (DictItem['title']), description=u'%s' % (DictItem['digest']),
                            image=u'%s' % (DictItem['thumb_url']), url=u'%s' % (DictItem['url']))
        writer.commit()
