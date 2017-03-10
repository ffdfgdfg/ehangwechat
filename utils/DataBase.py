# coding=utf-8
#数据库处理

import pymongo
import config

'''
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(40))
    nickname = Column(String(40))
    type = Column(String(20))

class oplog(Base):
    __tablename__ = 'oplog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    materialcount = Column(Integer)
    materialuptime = Column(Integer)

class comlog(Base):
    __tablename__ = 'comlog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(40))
    msg = Column(String)
    reply = Column(String)

class signlog(Base):
    __tablename__ = 'signlog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(40))
    student_id = Column(String(40))
    student_name = Column(String(40))

class adminauth(Base):
    __tablename__ = 'adminauth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(40))
    password = Column(String(40))
    access = Column(String(10))
'''

class MongoUtil:
    def __init__(self, db_host=config.databasesettings['host'], db_name=config.databasesettings['dbname']):
        self.db_ip = db_host
        self.db_name = db_name

        self.client = pymongo.MongoClient(self.db_ip, config.databasesettings['port']) # 并没有用账号和密码 ！！
        self.db = self.client[db_name] #选择数据库

        #（表单） 合集
        self.db_user_collection = 'user'
        self.db_oplog_collection = 'oplog'
        self.db_comlog_collection = 'comlog'
        self.db_signlog_collection = 'signlog'
        self.db_adminauth_collection = 'adminauth'

        # 建立合集连接
        self.user_collection = self.db[self.db_user_collection]
        self.oplog_collection = self.db[self.db_oplog_collection]
        self.comlog_collection = self.db[self.db_comlog_collection]
        self.signlog_collection = self.db[self.db_signlog_collection]
        self.adminauth_collection = self.db[self.db_adminauth_collection]

    def __del__(self):
        self.client.close()

    def NewbeeStr(self, OldStr, EndStr):
        return 'self.%s_collection.%s' % (OldStr, EndStr)

    def insert(self, CollectionName, *args, **kwargs):
        new = kwargs
        TreeNewbeeStr = self.NewbeeStr(CollectionName, 'insert(new)')
        exec (TreeNewbeeStr)

    def delete(self, CollectionName, by, *args, **kwargs):
        TreeNewbeeStr = self.NewbeeStr(CollectionName, "remove({'%s': kwargs[by]})" % (by))
        exec(TreeNewbeeStr)
    def prequery(self, CollectionName, by, *args, **kwargs):
        #也可以来计数     .count()
        TreeNewbeeStr = self.NewbeeStr(CollectionName, "find({'%s': kwargs[by]})" % (by))
        return exec(TreeNewbeeStr)
    def query(self, CollectionName, by, *args, **kwargs):
        result=self.prequery(CollectionName=CollectionName, by=by, kwargs=kwargs)
        if result.count() == 0:
            return None
        else:
            return result[0]
    def update(self, CollectionName, by, *args, **kwargs):
        #其实为upsert，update+insert
        updated = kwargs
        TreeNewbeeStr = self.NewbeeStr(CollectionName, "update({'%s': kwargs[by]}, updated, upsert=True)" % (by))
        exec(TreeNewbeeStr)
