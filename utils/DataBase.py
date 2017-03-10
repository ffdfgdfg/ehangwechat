# coding=utf-8
#数据库处理
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

# 创建对象的基类:
Base = declarative_base()

#建立数据表对象
# 定义User对象:
class user(Base):
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

#数据库操作类
class DBcontrol:
    __doc__ = '''有增删查改的方法，对应于数据表'''
    def __init__(self):
        # 数据库连接配置
        data = "%s+%s://%s:%s@%s:%s/%s" % \
               (config.dbtype, config.dbdrivername, config.dbusername, config.dbpassword, config.dbhost,
                config.dbport, config.dbname)
        # 初始化数据库连接:
        engine = create_engine(data)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        # 创建表单，有就跳过
        Base.metadata.create_all(engine)
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭session:
        self.session.close()

    def insert(self, tablename, *args, **kwargs):
        #增加方法，tablename表名，kwargs传入表单对应的量
        if tablename == 'user':
            new = user(openid=kwargs['openid'], nickname=kwargs['nickname'], type=kwargs['type'])
        elif tablename == 'oplog':
            new = oplog(materialcount=kwargs['materialcount'])
        elif tablename == 'comlog':
            new = comlog(openid=kwargs['openid'], msg=kwargs['msg'], reply=kwargs['reply'])
        elif tablename == 'signlog':
            new = signlog(openid=kwargs['openid'], student_id=kwargs['student_id'], studen_name=kwargs['student_name'])
        elif tablename == 'adminauth':
            new = signlog(username=kwargs['username'], password=kwargs['password'], access=kwargs['access'])
        else:
            new = None
        self.session.add(new)
        # 提交即保存到数据库:
        self.session.commit()
    def delete(self, tablename, by, *args, **kwargs):
        #删除方法
        DeleteItem=self.query(tablename=tablename, by=by, kwargs=kwargs)
        self.session.delete(DeleteItem)
        self.session.commit()
    def query(self, tablename, by, *args, **kwargs):
        #查询方法
        if tablename == 'user':
            if by == 'openid':
                result = self.session.query(user).filter(user.openid == kwargs[by])
            elif by == 'nikename':
                result = self.session.query(user).filter(user.nickname == kwargs[by])
            elif by == 'type':
                result = self.session.query(user).filter(user.type == kwargs[by])
            elif by == 'id':
                result = self.session.query(user).filter(user.id == kwargs[by])
            else:
                result = None
        elif tablename == 'oplog':
            if by == 'materialcount':
                result = self.session.query(oplog).filter(oplog.materialcount == kwargs[by])
            elif by == 'id':
                result = self.session.query(oplog).filter(oplog.id == kwargs[by])
            else:
                result = None
        elif tablename == 'comlog':
            if by == 'openid':
                result = self.session.query(comlog).filter(comlog.openid == kwargs[by])
            elif by == 'id':
                result = self.session.query(comlog).filter(comlog.id == kwargs[by])
            else:
                result = None
        elif tablename == 'signlog':
            if by == 'openid':
                result = self.session.query(signlog).filter(signlog.openid == kwargs[by])
            elif by == 'student_id':
                result = self.session.query(signlog).filter(signlog.student_id == kwargs[by])
            elif by == 'student_name':
                result = self.session.query(signlog).filter(signlog.student_name == kwargs[by])
            else:
                result = None
        elif tablename == 'adminauth':
            if by == 'username':
                result = self.session.query(adminauth).filter(adminauth.username == kwargs[by])
            elif by == 'id':
                result = self.session.query(adminauth).filter(adminauth.id == kwargs[by])
            elif by == 'access':
                result = self.session.query(adminauth).filter(adminauth.access == kwargs[by])
        else:
            result = None
        return result
    def update(self, tablename, by, how, *args, **kwargs):
        #修改方法
        update_target=self.query(tablename, by, kwargs=kwargs)

        if tablename == 'user':
            if how == 'openid':
                update_target.openid = kwargs[how]
            elif how == 'nikename':
                update_target.nickname = kwargs[how]
            elif how == 'type':
                update_target.type = kwargs[how]
            else:
                update_target = None
        elif tablename == 'oplog':
            if how == 'materialcount':
                update_target.materialcount = kwargs[how]
                update_target.materialuptime = kwargs[how]
            else:
                update_target = None
        elif tablename == 'signlog':
            if how == 'openid':
                update_target.openid = kwargs[how]
            elif how == 'student_id':
                update_target.student_id = kwargs[how]
            elif how == 'student_name':
                update_target.student_name = kwargs[how]
            else:
                update_target = None
        elif tablename == 'adminauth':
            if how == 'access':
                update_target.access = kwargs[how]
            elif how == 'password':
                update_target.password = kwargs[how]
            else:
                update_target = None
        else:
            update_target = None
        self.session.merge(update_target)  # 使用merge方法,如果存在则修改,如果不存在则插入
        self.session.commit()