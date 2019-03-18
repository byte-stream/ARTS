## Basic Auth 鉴权

最近遇到两个服务之间需要通过接口获取数据的需求，在讨论后选择了Basic Auth 的鉴权方式。

Basic Auth，顾名思义就是基础的鉴权，毕竟是内部接口，加上鉴权主要是为了防止犯蠢，比如测试环境调用了生产环境。

### 生成token

Basic Auth的Token生成十分简单，base64后的`username:password` ，加上Basic前缀即可。

这里只要跟对方约定好不同环境的username与password即可

```python
import base64

base64.b64encode('arts:the-password'.decode())  # YXJ0czp0aGUtcGFzc3dvcmQ=
```

拿到生成的token后，只需要在对应的接口请求头中加上 `Authorization='Basic YXJ0czp0aGUtcGFzc3dvcmQ='`即可

### 解析token

如果是使用数据库中的账号密码，而不是口头约定，其实还可以进一步校验。

```python
import base64


base64.b64decode(b'YXJ0czp0aGUtcGFzc3dvcmQ=')  # arts:the-password
```

解析token后，将username，password去库中对比即可

> 具体应用视情况而定