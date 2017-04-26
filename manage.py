#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
from werkzeug.security import generate_password_hash
from apps import config
from apps.init_app import app, mongo
from flask_script import Manager
__author__ = "Allen Woo"

manager = Manager(app)

@manager.command
def init_site():

    '''
    初始化root用户角色, 管理员, 管理员基本资料
    :return:
    '''
    # 创建超级用户角色,存在则不创建
    print('第一个管理员用户初始化')
    username = raw_input("输入用户名:")
    email = raw_input("输入email:")

    password = raw_input("输入密码,至少8个字符:")
    print('创建数据库库collection')
    try:
        print('创建role collection...')
        mongo.db.create_collection("role")
    except:
        pass
    try:
        print('创建user collection...')
        mongo.db.create_collection("user")
    except:
        pass

    role_root = mongo.db.role.find_one({"permissions":config.Role.ROOT})
    if not role_root:
        print("创建role角色...")
        _id = mongo.db.role.insert({
            "name":"Root",
            "default":False,
            "permissions":config["permission"].ROOT,
            "instructions":'ROOT',

        })
    else:
        role_id = role_root['_id']

    password_hash = generate_password_hash(password)
    root_user = mongo.db.user.find_one({"$or":[{"username":username}, {"email":email}]})
    if root_user:
        mongo.db.user.update({"_id":root_user["_id"]},{"$set":{"password":password_hash}})
    else:
        print('创建ROOT用户...')
        user = {"username":username.strip(),
                "email":email.strip(),
                "password":password_hash,
                "create_at":time.time(),
                "role_id":role_id
                }
        mongo.db.user.insert(user)

    print('刚创建的用户登录信息如下:')
    print("用户名:{}\nEmail:{}\n".format(username, email))

if __name__ == "__main__":
    manager.run()
