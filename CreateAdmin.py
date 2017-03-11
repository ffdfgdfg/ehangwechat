# -*- coding: utf-8 -*-
from utils import DataBase
db = DataBase.MongoUtil()
Admin={
    #修改username 和password后面的值即可
    'username':'xxxxx',
    'password':'xxxxx',
}
if len(Admin) is not 0 and len(Admin['username']) is not 0 and len(Admin['password']) is not 0:
    db.insert(CollectionName='adminauth', username=Admin['username'], password=Admin['password'])
    print('添加用户%s,成功' % Admin['username'])
else:
    print('添加失败')