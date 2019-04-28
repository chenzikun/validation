# 校验器扩展

## 1. 快速入门

支持两种使用方式：
- request_validation: 装饰器模式
- ValidatorManager： flask扩展插件模式

### 装饰器模式 request_validation

#### 服务端
```python
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return "hello"


@app.route("/index", methods=["GET", "POST"])
@request_validation(server_type="auth")
def hello():
    re = {"code": -123, "message": "hello"}
    return jsonify(re)
```

#### 客户端发送请求

```python
data = {
        "apikey": "di2kd92lsdf92.o23o3sf233lkjsf.sdfkjo2i3lkjsldkfj234df",
        # "source": "xxx",
        "deviceId": "xxx",
        "deviceVersion": "xxx",
        "sdkVersion": "1.0.0",
        "requestId": "abcdef",
}

rv = requests.post("/index", data=json.dumps(data))
res = json.loads(rv.data)

assert res["code"] == 1001
assert res["message"] == ""
```

#### 目前支持的type列表

```python
# register_funcs.py
ServerType = {
    ...
}
```

### 插件模式 ValidatorManager

flask 插件

#### 注册全局检验

```python
app = Flask(__name__)
app.validator_manager = ValidatorManager(app)

validator = RequestValidator("name", required=True)
app.validator_manager.register_global_validator(validator)
```

#### 注册蓝图级别检验
```python
app = Flask(__name__)
app.validator_manager = ValidatorManager(app)

param_bp = Blueprint("param", __name__, )

validator = RequestValidator("name", required=True)
app.validator_manager.register_blueprint_validator(param_bp, validator)
````


## 2. request_validation

基于flask请求的校验器封装

参数：
- key: 校验值
- validator：校验器
- required：是否是必须参数
- error: 自定义error

### 如何定义自己的校验

RequestValidator是对key对应的值进行校验，它封装了数据， 校验key是否是必须的，校验器。

当`required=True`时, request请求数据无指定的key时，会直接返回异常给客户端

当key不是必须的时候，只有在获得值时才进行校验

```python
validator = OneOf(REQUEST_ALLOWED_SOURCE)
request_validator = RequestValidator(key="source", required=True, validator=validator)
```

### 自定义error

默认会抛出系统异常， 你也可以自定义异常，但需要继承JSONRPCError

```python
class JSONRPCValidationError(JSONRPCError):
    CODE = -1234
    MESSAGE = "Validation Error"

validator = OneOf(REQUEST_ALLOWED_SOURCE)
request_validator = RequestValidator(key="source", required=True, validator=validator， error=JSONRPCValidationError)

```
### 自定义数据来源

```python
validator = OneOf(REQUEST_ALLOWED_SOURCE)
value = request.form.get("key")
request_validator = RequestValidator(key="source", required=True, validator=validator，value=value)
```

单独使用时，请捕获异常



## JSONRPCError

JSONRPC异常基类，Exception子类

error.json 返回json格式响应数据

----

## Validator

校验器， 可单独使用

## ValidationError

校验异常

