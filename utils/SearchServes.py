import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer

class Serves:
    def __init__(self):
        pass
    def __enter__(self):
        # 搜索对象的方法
        # 使用结巴中文分词
        analyzer = ChineseAnalyzer()
        # 创建schema, stored为True表示能够被检索
        schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                        description=TEXT(stored=True, analyzer=analyzer),
                        image=TEXT(stored=False),
                        url=TEXT(stored=False))
        # 存储schema信息至'indexdir'目录下
        indexdir = 'indexdir/'
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        self.ix = create_in(indexdir, schema)
    def search(self, key):
        # 创建一个检索器
        searcher = self.ix.searcher()
        # 检索标题中出现'文档'的文档
        return searcher.find("title", u'%s' % (key) or "description", u'%s' % (key))
    def AddIndex(self, DictItem):
        #添加检索列表
        # 按照schema定义信息，增加需要建立索引的文档
        # 注意：字符串格式需要为unicode格式
        writer = self.ix.writer()
        writer.add_document(title=u'%s' % (DictItem['title']), description=u'%s' % (DictItem['digest']),
                            image=u'%s' % (DictItem['thumb_media_id']), url=u'%s' % (DictItem['media_id']))
        writer.commit()