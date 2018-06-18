#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
业务封装
"""

# ----------------COMMON REQUEST VALIDATOR-------------------

# from request_validator import RequestValidator
# from validators import OneOf, IsaAlphaNumber
# from config import REQUEST_ALLOWED_SOURCE
from validations.config import REQUEST_SOURCE_ALLOWED, THREADS_MODES_ALLOWED, COLLECT_FILE_TYPES_ALLOWED, \
    THREADS_IPS_MODES_ALLOWED
from validations.request_validator import RequestValidator
from validations.validators import OneOf, IsaAlphaNumber


def create_source_validators():
    """source"""
    validator = OneOf(REQUEST_SOURCE_ALLOWED)
    request_validator = RequestValidator(key="source", required=True, validator=validator)
    return request_validator


def create_device_id_validator():
    """ deviceId"""
    validator = IsaAlphaNumber(".+_ ")
    request_validator = RequestValidator(key="deviceId", required=True, validator=validator)
    return request_validator


def create_device_version_validator():
    """deviceVersion"""
    validator = IsaAlphaNumber(".+_ ")
    request_validator = RequestValidator(key="deviceVersion", required=True, validator=validator)
    return request_validator


def create_token_validator():
    """token"""
    token_val = IsaAlphaNumber(".+_ ")
    token_request_val = RequestValidator(key="token", required=True, validator=token_val)
    return token_request_val


def create_file_validator():
    """file"""
    file_request_validator = RequestValidator(key="file", required=True)
    return file_request_validator


# --------- 可选参数 ------------

def create_sdk_version_validator():
    """sdk_validator 可选参数"""
    validator = IsaAlphaNumber(".+_ ")
    sdk_version_val = RequestValidator(key="sdkVersion", validator=validator)
    return sdk_version_val


def create_request_id_validator():
    """request_id 可选参数"""
    validator = IsaAlphaNumber(".+_ ")
    request_id_val = RequestValidator(key="requestId", validator=validator)
    return request_id_val


def create_extend_validator():
    return RequestValidator(key="extend")


# ----------------SOAPA APP-------------------


def register_auth_validators():
    """登录校验"""

    apikey_val = IsaAlphaNumber(".+_ ")
    api_key_request_val = RequestValidator(key="apikey", required=True, validator=apikey_val)
    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (api_key_request_val, source_validators, device_id_validator, device_version_validator,
            request_id_val, sdk_version_val, extend_val)


def register_domain_validators():
    """domains云查"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    domain_request_val = RequestValidator(key="domains", required=True)

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, domain_request_val,
            request_id_val, sdk_version_val, extend_val)


def register_url_validators():
    """URL云查"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    url_request_val = RequestValidator(key="urls", required=True)

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, url_request_val,
            request_id_val, sdk_version_val, extend_val)


def register_ips_validators():
    """ips 查询"""
    # todo 暂不提供
    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    # todo 样式校验 ips json
    ips_request_val = RequestValidator(key="ips", required=True)

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, ips_request_val,
            request_id_val, sdk_version_val, extend_val)


def register_file_hash_validator():
    """file hash"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    file_request_val = RequestValidator(key="fileMd5s", required=True)

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, file_request_val,
            request_id_val, sdk_version_val, extend_val)


def register_file_scan_validator():
    """file扫描"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    file_validator = create_file_validator()

    md5_validator = IsaAlphaNumber(" ")
    md5_val = RequestValidator(key="md5", validator=md5_validator)
    sdk_version_val = create_sdk_version_validator()
    file_path_val = RequestValidator(key="filePath")
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, file_validator,
            md5_val, sdk_version_val, file_path_val, extend_val)


def register_safe_events_validators():
    """安全事件 type=url"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()

    request_id_val = create_request_id_validator()
    sdk_version_validator = create_sdk_version_validator()
    extend_val = create_extend_validator()
    validator = IsaAlphaNumber()
    incident_id_val = RequestValidator(key="incidentId", validator=validator)

    return (source_validators, device_id_validator, device_version_validator, token_validator, request_id_val,
            sdk_version_validator, extend_val, incident_id_val)


def register_threats_intelligence_validators():
    """威胁情报: 域名 & URL & 文件 type=url
    """

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    modes_validator = OneOf(THREADS_MODES_ALLOWED)
    mode_request_validator = RequestValidator(key="mode", required=True, validator=modes_validator)
    number_request_val = RequestValidator(key="number", required=True)

    validator = IsaAlphaNumber(".+_ ")
    version_val = RequestValidator(key="version", validator=validator)
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, mode_request_validator,
            number_request_val, version_val, sdk_version_val, extend_val
            )


def register_threats_ips_validators():
    """威胁情报: IP
    """
    # todo 暂不提供
    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    modes_validator = OneOf(THREADS_IPS_MODES_ALLOWED)
    mode_request_validator = RequestValidator(key="mode", required=True, validator=modes_validator)
    number_request_val = RequestValidator(key="number", required=True)

    validator = IsaAlphaNumber(".+_ ")
    version_val = RequestValidator(key="version", validator=validator)
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (source_validators, device_id_validator, device_version_validator, token_validator, mode_request_validator,
            number_request_val, version_val, sdk_version_val, extend_val
            )


def register_collect_files_validators():
    """数据采集 文件 type=url"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    types_validator = OneOf(COLLECT_FILE_TYPES_ALLOWED)
    file_type_request_val = RequestValidator(key="type", required=True, validator=types_validator)

    file_validator = create_file_validator()

    validator = IsaAlphaNumber(".+_ ")
    file_name_val = RequestValidator(key="fileName", validator=validator)
    sdk_version_val = create_sdk_version_validator()
    request_id_val = create_request_id_validator()
    extend_val = create_extend_validator()

    return (source_validators, device_id_validator, device_version_validator, token_validator, file_type_request_val,
            file_validator, sdk_version_val, file_name_val, request_id_val, extend_val)


def register_collect_logs_validators():
    """ 数据采集 logs type=url"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    logs_request_val = RequestValidator(key="logs", required=True)

    request_id_val = create_request_id_validator()
    sdk_version_val = create_sdk_version_validator()
    extend_val = create_extend_validator()
    return (
        source_validators, device_id_validator, device_version_validator, token_validator, logs_request_val,
        request_id_val, sdk_version_val, extend_val)


def register_file_issued_validators():
    """ 文件下发 type=url"""

    source_validators = create_source_validators()
    device_id_validator = create_device_id_validator()
    device_version_validator = create_device_version_validator()
    token_validator = create_token_validator()
    validator = IsaAlphaNumber(".+_ ")
    file_version_request_val = RequestValidator(key="fileVersion", required=True, validator=validator)

    extend_val = create_extend_validator()
    sdk_version_val = create_sdk_version_validator()

    return (source_validators, device_id_validator, device_version_validator, token_validator, file_version_request_val,
            sdk_version_val, file_version_request_val, extend_val)


ServerType = {
    "auth": register_auth_validators,
    "domain": register_domain_validators,
    "url": register_url_validators,
    "ips": register_ips_validators,
    "file_hash": register_file_hash_validator,
    "file_scan": register_file_scan_validator,
    "safe_events": register_safe_events_validators,
    "threats_intelligence": register_threats_intelligence_validators,
    "collect_files": register_collect_files_validators,
    "collect_logs": register_collect_logs_validators,
    "file_issued": register_file_issued_validators
}
