#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = "Allen Woo"

class Role():
    '''
    用户角色权重,使用二进制
    '''
    PERMISSIONS = [
        ("USER",0b00000001), #普通用户
        ("ADMIN",0b01000000), #管理员
        ("ROOT",0b10000000) #超级管理员
    ]


