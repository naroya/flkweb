#!/usr/bin/env python
# -*-coding:utf-8-*-
from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import abort

__author__ = "Allen Woo"

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 如何不能高这个权重,则返回404
            if not current_user.can(permission):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
