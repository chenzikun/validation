#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校验器及校验器异常
"""

import re

__author__ = "chenzikun"


# ------------validator Error-----------------------
# TODO 编写校验器异常


class ValidationError(Exception):
    """ 校验器Error基类
    """
    default_message = "ValidationError"

    def __init__(self, message=None):
        error = message if message else self.default_message
        super(ValidationError, self).__init__(error)


class ValidationRegexpError(ValidationError):
    """ 正则匹配异常
    """
    default_message = 'string is not match pattern'

    def __init__(self, message=None):
        super(ValidationRegexpError, self).__init__(message=message)


class ValidationOneOfError(ValidationError):
    """ value不在期待的范围异常
    """
    default_message = 'your put is not expected'

    def __init__(self, message=None):
        super(ValidationOneOfError, self).__init__(message=message)


# ------------validator-----------------------
# TODO 编写校验器

class Validator(object):
    """校验器基类"""

    def _repr_args(self):
        return ''

    def __repr__(self):
        args = self._repr_args()
        args = '{0}, '.format(args) if args else ''

        return ('<{self.__class__.__name__}({args})>'.format(self=self, args=args))


class Regexp(Validator):
    """ 正则表达式校验器

    """

    def __init__(self, regex, flags=0):
        self.regex = re.compile(regex, flags)

    def _repr_args(self):
        return 'regex={0!r}'.format(self.regex)

    def _format_error(self, value):
        return "{} does not match expected pattern {}".format(value, self.regex)

    def __call__(self, value):
        if self.regex.match(value) is None:
            raise ValidationError(self._format_error(value))
        return True


class IsaAlphaNumber(Validator):
    """ 字母、数字、空格

    """

    def __init__(self, chars=None):
        if chars:
            assert isinstance(chars, str)
            chars = list(chars)
        self.chars = chars

    def _format_error(self, value):
        return "{value} is not alpha or num".format(value=value)

    def __call__(self, value):
        if self.chars:
            for char in self.chars:
                value = value.replace(char, "")
        if not value.isalnum():
            raise ValidationError(self._format_error(value))
        return True


class OneOf(Validator):
    """Validator which if ``value`` is a member of ``iterable``.

    :param iterable iterable: A sequence of invalid values.
    """

    def __init__(self, iterable):
        self.iterable = iterable
        self.values_text = ', '.join(str(each) for each in self.iterable)

    def _repr_args(self):
        return 'iterable={0!r}'.format(self.iterable)

    def _format_error(self, value):
        return "Invalid input {input}, While Expected {values}'".format(
            input=value,
            values=self.values_text,
        )

    def __call__(self, value):
        if value not in self.iterable:
            raise ValidationOneOfError(self._format_error(value))
        return value
