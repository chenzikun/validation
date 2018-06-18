#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 参数校验器

"""

import six

from validations.validators import ValidationError

__author__ = "chenzikun"

from flask import g
import json


# --------------------JSONRPC exception---------------------------------------------
# todo 编写异常码
#
class JSONRPCError(Exception):
    """JSONRPC 异常基类

    提供方法json将错误信息返回
    """
    serialize = staticmethod(json.dumps)
    deserialize = staticmethod(json.loads)

    def __init__(self, code=None, message=None, data=None):
        self._data = dict()
        self.code = getattr(self.__class__, "CODE", code)
        self.message = getattr(self.__class__, "MESSAGE", message)
        self.data = data

    def __get_code(self):
        return self._data["code"]

    def __set_code(self, value):
        if not isinstance(value, six.integer_types):
            raise ValueError("Error code should be integer")

        self._data["code"] = value

    code = property(__get_code, __set_code)

    def __get_message(self):
        return self._data["message"]

    def __set_message(self, value):
        if not isinstance(value, six.string_types):
            raise ValueError("Error message should be string")

        self._data["message"] = value

    message = property(__get_message, __set_message)

    def __get_data(self):
        return self._data.get("data")

    def __set_data(self, value):
        if value is not None:
            self._data["data"] = value

    data = property(__get_data, __set_data)

    @classmethod
    def from_json(cls, json_str):
        data = cls.deserialize(json_str)
        return cls(
            code=data["code"], message=data["message"])

    @property
    def json(self):
        return self.serialize(self._data)


class JSONRPCValidationError(JSONRPCError):
    CODE = -1234
    MESSAGE = "Validation Error"


class JSONRPCKeyNotExist(JSONRPCError):
    """ Key NotExist

    The key is required while is not exist in request

    """
    CODE = -12345
    MESSAGE = "Key Is Not Exist!"


class JSONRPCRegexpError(JSONRPCError):
    """ RegexpError

    """
    CODE = -12345
    MESSAGE = "String not match pattern"


class JSONRPCOneOfError(JSONRPCError):
    CODE = -123435
    MESSAGE = "Your input is not expected"


class JSONRPCServerError(JSONRPCError):
    """ Server error.

    Reserved for implementation-defined server-errors.

    """

    CODE = -32000
    MESSAGE = "Server error"


class JSONRPCInvalidRequest(JSONRPCError):
    """ Invalid Request.

    The JSON sent is not a valid Request object.

    """

    CODE = 1001
    MESSAGE = "params wrong"


class JSONRPCUnknownError(JSONRPCError):
    """Unknown Error
    """
    CODE = 1000
    MESSAGE = "unknown error"

    def __init__(self, data=None):
        super(JSONRPCUnknownError, self).__init__(data=data)


# ----------------------------------------------------

class RequestValidator(object):
    def __init__(self, key, validator=None, required=False, error=None, name=None, value=None):
        """
        :param key:       想要校验的key
        :param validator: 校验器实例
        :param required:  字段key是否是必须的
        :param error:     如果校验异常，会抛出自定义的异常
        :param name:      校验器名
        :param value:     自定义数据，否则从key中获取对应的值
        """
        self.key = key
        self.validator = validator
        self.required = required
        self.name = name if name else self.validator.__class__.__name__
        self.error = error
        self._value = value

    @property
    def data(self):
        return g.kwargs

    @property
    def value(self):
        if self._value:
            return self._value
        return self.data.get(self.key)

    def validator_required(self):
        """ 校验required的属性
        """
        if self.required and self.key not in self.data.keys():
            raise JSONRPCKeyNotExist

    def validate(self, value):
        """ validate 校验行为 call validator.__call__
        :param value: 需要校验的值
        """
        return self.validator(value)

    def _call(self):
        self.validator_required()
        if self.validator:
            if self.value:
                return self.validate(self.value)
        return

    def handle_error(self, e):
        """异常处理"""
        if self.error:
            return self.error
        elif issubclass(e.__class__, JSONRPCError):
            raise JSONRPCInvalidRequest
        elif issubclass(e.__class__, ValidationError):
            raise JSONRPCInvalidRequest
        else:
            raise JSONRPCUnknownError

    def __call__(self):
        """ flask before request function
        """
        try:
            return self._call()
        except Exception as e:
            raise self.handle_error(e)

    def __repr__(self):
        return "<{}(key:{},validator:{})>".format(self.__class__.__name__, self.key, self.validator)
