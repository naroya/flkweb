#!/usr/bin/env python
# -*-coding:utf-8-*-
from apps.init_app import app
from flask_script import Manager
__author__ = "Allen Woo"

manager = Manager(app)
if __name__ == "__main__":
    manager.run()
