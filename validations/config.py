#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "chenzikun"

# 允许请求的来源
REQUEST_SOURCE_ALLOWED = [
    "USERRPT", "SIP", "SIP_SMTP", "SIP_SMB", "EDR", "EDR_BOTNET", "NGAF"
]

# 威胁情报modes
THREADS_MODES_ALLOWED = [
    "full", "update"
]

# 威胁情报 ips
THREADS_IPS_MODES_ALLOWED = [
    "complete", "patch"
]

# 文件采集type
COLLECT_FILE_TYPES_ALLOWED = [
    "NGAF_CONFIG", "NGAF_DNS", "NGAF_URL", "NGAF_MAIL", "NGAF_SECEVENT", "AC_URL", "SIP_MAIL", "SIP_SECEVENT"
]
