#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 校验器封装
提供两种使用方式：
一、使用request_validation装饰器，在每个视图函数中使用
二、使用ValidatorManager注册为flask的扩展
"""
import json
import types
from functools import wraps

from flask import g, request, current_app

from validations.register_funcs import ServerType
from validations.request_validator import JSONRPCInvalidRequest, JSONRPCServerError, JSONRPCError, JSONRPCUnknownError

__author__ = "chenzikun"


class DecoratorValidator(object):
    def __init__(self, func, server_type):
        wraps(func)(self)
        self.func = func
        self.server_type = server_type
        self._collect_validators = None

    @property
    def collect_validators(self):
        if not self._collect_validators:
            self._collect_validators = ServerType[self.server_type]()
        return self._collect_validators

    def _set_g(self):
        g.kwargs = {}
        if request.args:
            g.kwargs.update(request.args.items())
        if request.data:
            g.kwargs.update(json.loads(request.data))
        if request.form:
            g.kwargs.update(request.form.items())
        if request.files:
            g.kwargs.update(request.files.items())
        if not g.kwargs:
            raise JSONRPCInvalidRequest

    def __call__(self, *args, **kwargs):
        if self.server_type not in ServerType.keys():
            return JSONRPCServerError().json
        try:
            self._set_g()
            self.handle_validators()
            return self.func(*args, **kwargs)
        except JSONRPCError as e:
            return e.json
        except Exception as e:
            return JSONRPCUnknownError(data=e).json

    def handle_validators(self):
        for validator in self.collect_validators:
            validator()

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def request_validation(server_type):
    def decorator(func):
        return DecoratorValidator(func, server_type)

    return decorator


class ValidatorManager(object):
    """flask 校验器扩展
    demo:
        ValidatorManager(app)
        validator = RequestValidator("name", required=True)
        app.validator_manager.register_global_validator(validator)

    抛出 JSONRPCError类型将会被处理
    """

    def __init__(self, app=None, data=None):
        """
        :param app: app实例
        :param type: 数据源类型
            json   json参数格式, default
            url    url类型数据
        :param data: 可以传入数据类型，不从request中获取
        """
        self._app = app
        if app:
            self.init_app(app)
        if data:
            assert isinstance(data, dict)
        self.validators = []

    def init_app(self, app):
        if not hasattr(app, 'ValidatorExtension'):
            app.extensions = {}
        app.extensions.update({'ValidatorExtension': self})

        # 将校验数据源装载到flask.g中
        app.before_request(self._set_g)
        # 注册异常处理函数
        app.register_error_handler(JSONRPCError, self.make_error_response)

    @property
    def app(self):
        return self._app or current_app

    def _set_g(self):
        """校验数据源"""
        g.kwargs = {}
        if request.args:
            g.kwargs.update(request.args)
        if request.data:
            g.kwargs.update(json.loads(request.data))
        if request.form:
            g.kwargs.update(request.form.items())
        if request.files:
            g.kwargs.update(request.files.items())
        if not g.kwargs:
            raise JSONRPCInvalidRequest

    def register_global_validator(self, request_validator):
        """注册 global RequestValidator参数校验"""
        request_validator.__name__ = "global_" + request_validator.name
        self.app.before_request(request_validator)

    def register_blueprint_validator(self, blueprint, request_validator):
        """注册 blueprint RequestValidator参数校验"""
        request_validator.__name__ = blueprint.name + request_validator.name
        blueprint.before_request(request_validator)

    @staticmethod
    def make_error_response(error):
        """异常处理函数"""
        return error.json

    def __repr__(self):
        return "<{}(app:{})>".format(self.__class__.__name__, self.app.__name__)
