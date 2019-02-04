# 具有公钥签名的 Json Web Token

**本文为翻译**

**原文地址: https://blog.miguelgrinberg.com/post/json-web-tokens-with-public-key-signatures**

JSON  Web Tokens 提供了一种简单而高效的方式为 API 生成 token。这些 tokens 携带了一种被加密签名后的 payload。虽然 payload 本身没有加密，但签名会再次篡改它。在他们最常见的格式中，“密钥(secret key)” 用于签名的生成和验证。在本文中，我将向你展示一种不常见的生成 JWT 的机制，JWT 具有可以在不访问密钥的情况下进行验证的签名。

## JSON Web Token 快速入门

如果你对 JWTs 不熟悉，首先让我来告诉你如何在 Python 下使用 `pyjwt` 包。创建一个虚拟环境，并且安装 `pyjwt`：

```python
(venv)$ pip install pyjwt
```

现在假设你想要在你程序中，为一个 id 123 的用户创建 token。在验证了用户名和密码之后，你可以为该用户生成 token:

```python
>>> import jwt
>>> secret_key = "a random, long, sequence of characters that only the server knows"
>>> token = jwt.encode({'user_id': 123}, secret_key, algorithm='HS256').decode('utf-8')
>>> token
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.oF_jJKavmWrM6d_io5M5PBiK9AKMf_OcK4xpc17kvwI'
```

首先 `jwt.encode()` 方法有三个参数，其中最重要的是第一个参数，包含了 token payload。这是你想在 token 中存的信息。你可以使用任何能序列化成 JSON 字典作为 payload。payload 是你记录表示用户信息的地方。上面示例中的用户 ID 是最简单的情况，但是你可以包含其他用户信息，例如用户名、用户角色、权限等。这里有关于 token 更复杂的例子：

```python
>>> token = jwt.encode({
...    'user_id': 123,
...    'username': 'susan',
...    'roles': ['user', 'moderator']
...}, secret_key, algorithm='HS256').decode('utf-8')
>>> token
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoic3VzYW4iLCJyb2xlcyI6WyJ1c2VyIiwibW9kZXJhdG9yIl19.fRZ4ButrxgElKB57TlunFo4bGGHponRJcV54NMF-hgM'
```

正如你所看到的，你在 token 中写入的数据越多，生成的 token 就越长，这是因为数据只是简单地存储在 token 中。通过查看生成的 JWT，你可能会认为写入 token 中的数据已经加密了，其实这是错误的。你永远不应该在 JWT 中写入敏感的数据，因为并没有加密。在 token 中看到的看似随机的字符序列，只是使用简单的 base64 编码生成的。

除了用户信息之外，JWT 的 payload 还可以包含一些预设、用于 token 本身的字段。其中最用于的是 `exp` 字段，它定义了 token 的到期时间。下面的示例中为 token 提供了 5 分钟 (300秒) 的有效期：

```python
>>> from time import time
>>> token = jwt.encode({
...    'user_id': 123,
...    'username': 'susan',
...    'roles': ['user', 'moderator'],
...    'exp': time() + 300
...}, secret_key, algorithm='HS256').decode('utf-8')
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoic3VzYW4iLCJyb2xlcyI6WyJ1c2VyIiwibW9kZXJhdG9yIl0sImV4cCI6MTUyODU2MDc3My41Mzg2ODkxfQ.LuicSWptAYHBXKJnM3iz9V07Xz_vSKb3AheYXOC444A'
```

其他在包含 JWT 中预设的字段像 `nbf` (not before)，它定义了 token 变为有效的未来时间点。 `iss` (issuer)，`aud` (audience) 和 `iat` (issued at)。如果你想了解更多关于 JWT，可以访问 [JWT specification](https://tools.ietf.org/html/rfc7519)。

`jwt.encode()` 第二个参数是 secret key。这是在算法中使用的字符串，用于为 token 生成加密签名。我的想法是，只有程序才能知道此密钥，因为拥有此密钥的任何人都可以生成具有有效签名的新 token。在 Flask 或者 Django 程序中，你可以设置 `SECRET_KEY` 参数。

`jwt.encode()` 最后一个参数签名算法。许多程序使用 `HS256` 算法，它是 HMAC-SHA256 的简写。这个签名算法保护 JWT 中的 payload 不被篡改。

`jwt.encode()` 返回的值是字节序列 token。你看到在上面所有的例子中，token 解码都是用的 UTF-8 编码，这是因为对于字符串更容易解析。

一旦你的程序生成了 token，它必须将其返回给用户，在这之后，用户可以通过将 token 传给服务器来进行身份验证。这可以防止用户频繁地发送凭证，如用户名和密码。使用 JWT 进行身份验证被认为比用户名和密码更安全，因为你可以设置适当的过期时间，并可以防止密码泄露情况下造成的损失。

当程序从用户收到 JWT 时，它需要确保它是由程序本身生成的合法 token，这需要为 payload 生成新签名，并确保它与 token 中包含的签名匹配。使用上面第一个例子，这就是使用 pyjwt 验证的步骤：

```python
>>> import jwt
>>> secret_key = "a random, long, sequence of characters that only the server knows"
>>> token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.oF_jJKavmWrM6d_io5M5PBiK9AKMf_OcK4xpc17kvwI'
>>> payload = jwt.decode(token, secret_key, algorithms=['HS256'])
>>> payload
{'user_id': 123}
```

`jwt.decode()` 也需要三个参数：JWT token，签名密钥，和生成签名的算法。请注意，再次调用中如何提供 algorithm 参数，因为程序可能希望接受多个签名算法生成的 token。尽管 algorithm 参数在 pyjwt 中当前是可选的，但如果你没有明确的传递 algorithm 参数，则可能会出现 bug.如果你调用 `jwt.decode()` 的程序没有传递这个参数，我强烈建议你添加这个参数。

`jwt.decode()` 返回的值是 payload，它被作为字典存储在 token 中。如果此函数返回，则表示该 token 被确定为有效，因此可以将 payload 中的信息视为合法的。

让我们尝试从上面解码的时候，在 token 中带上过期时间。我生成的 token 超过 5 分钟了，因此即使它是正确的 token，现在也出错了因为它过期了：

```python
>>> token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoic3VzYW4iLCJyb2xlcyI6WyJ1c2VyIiwibW9kZXJhdG9yIl0sImV4cCI6MTUyODU2MDc3My41Mzg2ODkxfQ.LuicSWptAYHBXKJnM3iz9V07Xz_vSKb3AheYXOC444A'
>>> payload = jwt.decode(token, secret_key, algorithms=['HS256'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/migu7781/Documents/dev/flask/jwt-examples/venv/lib/python3.6/site-packages/jwt/api_jwt.py", line 105, in decode
    self._validate_claims(payload, merged_options, **kwargs)
  File "/Users/migu7781/Documents/dev/flask/jwt-examples/venv/lib/python3.6/site-packages/jwt/api_jwt.py", line 135, in _validate_claims
    self._validate_exp(payload, now, leeway)
  File "/Users/migu7781/Documents/dev/flask/jwt-examples/venv/lib/python3.6/site-packages/jwt/api_jwt.py", line 176, in _validate_exp
    raise ExpiredSignatureError('Signature has expired')
jwt.exceptions.ExpiredSignatureError: Signature has expired
```

如果我使用之前其中一个 token，对字符串中的任何字符进行更改，并尝试解码。它会发生什么情况：

```python
>>> token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.oF_jJKavmWrM6d_io5M5PBiK9AKMf_OcK4xpc17kvwO'
>>> payload = jwt.decode(token, secret_key, algorithms=['HS256'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/miguel/jwt/venv/lib/python3.6/site-packages/jwt/api_jwt.py", line 93, in decode
    jwt, key=key, algorithms=algorithms, options=options, **kwargs
  File "/home/miguel/jwt/venv/lib/python3.6/site-packages/jwt/api_jws.py", line 157, in decode
    key, algorithms)
  File "/home/miguel/jwt/venv/lib/python3.6/site-packages/jwt/api_jws.py", line 224, in _verify_signature
    raise InvalidSignatureError('Signature verification failed')
jwt.exceptions.InvalidSignatureError: Signature verification failed
```

正如你所见，如果 `jwt.decode()` 返回一个字典，你可以确定该字典中的数据是合法的，并且可以被信任的 (至少和你确定的 secret key 一样多)。

## 在 JWT 中使用公钥

流行的 HS256 签名算法的缺点是在生成和验证的时候都需要访问密钥。对于单一程序而言，这不是一个问题，但如果你有一个由多个服务构建的分布式系统，彼此独立运行，你必须在两个糟糕的选择之间进行选择：

- 你可以选择使用专用服务进行 token 的生成和验证。从客户端接收 token 的任何服务，都需要调用身份验证服务来验证 token。对于繁忙的系统来说，这会在身份验证服务上产生性能问题。
- 你可以为所有需要从客户端接收 token 的服务配置密钥，以便它们可以验证 token，无需调用身份验证服务。但是，在多个地方使用密钥会增加其受到攻击的风险，并且一旦受到攻击，攻击者就可以生成有效 token 并模拟系统中的任何用户。

因此对于这些程序，最好将签名密钥安全存储在身份验证服务中，并且仅用于生成密钥，而其他所有服务无需访问密钥就可以验证这些 token。实际上，这可以通过公钥加密来实现。

公钥加密基于两个组件的加密密钥：一个公钥和一个私钥。在命名实现时，公钥组件可以自由共享。可以使用公钥加密来完成两个工作流程：

- 消息加密：如果你想要向某人发送加密消息，我可以使用他的公钥来加密。加密的消息只能用他的私钥来解密。
- 消息签名：如果我想要签署一条消息它来自我，我可以使用自己的私钥来生成签名。任何对验证消息感兴趣的人，都可以使用我的公钥来确认签名是否有效。

JWT 的签名算法实现了上面的第二种情况。使用服务器的私钥对 token 进行签名，然后任何使用服务器公钥的人都可以验证它们，任何想要拥有它的人都可以免费使用。举个例子来说下面，我使用 `RS256` 签名算法，它是 RSA-SHA256 的简写。

`pyjwt` 包没有直接实现更高级的公钥签名算法的加密签名功能，而是依赖于 `cryptography`  包来提供这些。所以为了使用公钥签名，这个包需要安装：

```python
(venv)$ pip install cryptography 
```

下一步是为程序生成公钥/私钥集 (通常称为 "秘钥对")。生成 RSA 密钥有几种不同的方法，但我喜欢使用 openssh 中的 ssh-keygen 工具：

```python
(venv) $ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/miguel/.ssh/id_rsa): jwt-key
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in jwt-key.
Your public key has been saved in jwt-key.pub.
The key fingerprint is:
SHA256:ZER3ddV4/smE0rnoNesS+IwCNSbwu5SThfiWWtLYRVM miguel@MS90J8G8WL
The key's randomart image is:
+---[RSA 4096]----+
|       .+E. ....=|
|   .   + . .  ..o|
|    + o +   . oo |
|   . + O   . + ..|
|    = @ S . o + o|
|   o #   . o + o.|
|    * +   = o o  |
|   . . . . = .   |
|        .   o.   |
+----[SHA256]-----+
```

`ssh-keygen` 命令的 -t 选项定义了，我正在请求的秘钥对，-b 选项指定密钥大小为 4096 位，这被认为是一个非常安全的密钥长度。当你运行该命令时，系统提示你需要为秘钥对提供文件名，这里我在当前路径下使用 `jwt-key` 。然后，系统将提示你输入密码来保护密钥，密钥需要保留为空。

当运行完命令，你会在当前目录下获得两个文件，`jwt-key` 和 `jwt-key.pub`。前者是私钥，将用于生成 token 签名，因此你需要保存好它。特别是，你不应该将私钥提交到代码仓库，而应直接在服务器上安装 (如果你需要重建服务器，则应做好备份)。.pub 文件用于验证 token。由于此文件没有敏感信息，因此你可以在需要验证 token 的任何项目上随意添加该文件的副本。

使用此秘钥对生成 token 的过程与我之前的内容非常相似。我们先创建一个新的 token:

```python
>>> import jwt
>>> private_key = open('jwt-key').read()
>>> token = jwt.encode({'user_id': 123}, private_key, algorithm='RS256').decode('utf-8')
>>> token
'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.HT1kBSdGFAznrhbs2hB6xjVDilMUmKA-_36n1pLLtFTKHoO1qmRkUcy9bJJwGuyfJ_dbzBMyBwpXMj-EXnKQQmKlXsiItxzLVIfC5qE97V6l6S0LzT9bzixvgolwi-qB9STp0bR_7suiXaON-EzBWFh0PzZi7l5Tg8iS_0_iSCQQlX5MSJW_-bHESTf3dfj5GGbsRBRsi1TRBzvxMUB6GhNsy6rdUhwoTkihk7pljISTYs6BtNoGRW9gVUzfA2es3zwBaynyyMeSocYet6WJri97p0eRnVGtHSWwAmnzZ-CX5-scO9uYmb1fT1EkhhjGhnMejee-kQkMktCTNlPsaUAJyayzdgEvQeo5M9ZrfjEnDjF7ntI03dck1t9Bgy-tV1LKH0FWNLq3dCJJrYdQx--A-I7zW1th0C4wNcDe_d_GaYopbtU-HPRG3Z1SPKFuX1m0uYhk9aySvkec66NBfvV2xEgo8lRZyNxntXkMdeJCEiLF1UhQvvSvmWaWC-0uRulYACn4H-tZiaK7zvpcPkrsfJ7iR_O1bxMPziKpsM4b7c7tmsEcOUZY-IHEI9ibd54_A1O72i08sCWKT5CXyG70MAPqyR0MFlcV7IuDtBW3LCqyvfsDVk4eIj8VcSU1OKQJ1Gl-CTOHEyN-ncV3NslVLaT9Q1C4E7uK2QpS8z0'
```

和之前 token 主要区别在于我将 RSA 私钥作为密钥参数传递，该键的值是 `jwt-key` 的全部内容。另外不同的是算法是 `RS256`。生成的 token 更长，但与我之前生成的 token 相似。与之前的 token 类似， payload 没有加密，因此你不应该把敏感信息放在 payload 里。

现在我拿到了 token，我将向你演示怎么通过公钥来验证的。如果你也在尝试，请退出 Python 会话并开始一个新会话，以确保 Python 上下文没有私钥的跟踪。以下是验证上述 token 的方法：

```python
>>> import jwt
>>> public_key = open('jwt-key.pub').read()
>>> token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjoxMjN9.HT1kBSdGFAznrhbs2hB6xjVDilMUmKA-_36n1pLLtFTKHoO1qmRkUcy9bJJwGuyfJ_dbzBMyBwpXMj-EXnKQQmKlXsiItxzLVIfC5qE97V6l6S0LzT9bzixvgolwi-qB9STp0bR_7suiXaON-EzBWFh0PzZi7l5Tg8iS_0_iSCQQlX5MSJW_-bHESTf3dfj5GGbsRBRsi1TRBzvxMUB6GhNsy6rdUhwoTkihk7pljISTYs6BtNoGRW9gVUzfA2es3zwBaynyyMeSocYet6WJri97p0eRnVGtHSWwAmnzZ-CX5-scO9uYmb1fT1EkhhjGhnMejee-kQkMktCTNlPsaUAJyayzdgEvQeo5M9ZrfjEnDjF7ntI03dck1t9Bgy-tV1LKH0FWNLq3dCJJrYdQx--A-I7zW1th0C4wNcDe_d_GaYopbtU-HPRG3Z1SPKFuX1m0uYhk9aySvkec66NBfvV2xEgo8lRZyNxntXkMdeJCEiLF1UhQvvSvmWaWC-0uRulYACn4H-tZiaK7zvpcPkrsfJ7iR_O1bxMPziKpsM4b7c7tmsEcOUZY-IHEI9ibd54_A1O72i08sCWKT5CXyG70MAPqyR0MFlcV7IuDtBW3LCqyvfsDVk4eIj8VcSU1OKQJ1Gl-CTOHEyN-ncV3NslVLaT9Q1C4E7uK2QpS8z0'
>>> payload = jwt.decode(token, public_key, algorithms=['RS256'])
>>> payload
{'user_id': 123}
```

这个例子与之前的例子看起来类似，但重要的是我们确保此 token 有效而无法访问任何敏感信息。服务器的公钥不存在风险，因此可以与世界自由分享。实际上，任何人都可以使用此密钥验证程序生成的 token。为了证明这一点，我把我的公钥分享给你：

```python
>>> public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCcjWidoIPNRc3IN1hoGeOdSvDkBDK3W3P7/4HxLf62nvUQVczL3FG+dG9KSRnzuvRoUi1o3TASO3Yn72FSfaLPE/JmOtpu/IGuB/oF/CrJqEHA/08n0xkNQK8kwdIqayKPS84PVOm8XomNijMpUCahqu9cGZDPhlgqD8PAxw4e1ZQSizWj0hTSCR78dmHAEr5oXryP6uD0Mw/KGKYel/KTMu00dShWPzHnJeLaYvKgMJKPN6pqhsWFQsNUDnKd9tgn3NSPeHECnnBbUxB2BeuVz72+HnyFWah3mpGH4Dr+9rjRXiPg2AYxgR3U93AEQ6osefxeIKUSCXWx1txNV07QzwFVag4vPBmrA9XktC7i5EP91wxUOsyzhG8geXKuDHmE+/7U3AsExHYFkBLqMnW92CaTeQ408xsRXjxWjSNHpfqhZVxGY5Eh8L3NVqgRg1LdnZYHpovi1iP4Zx2Z7Nb5F9ejuMsA+v/D0WL3c6bhwU8BKdD7YZDG2tpzq6PHt+NarGkcWWh9/p/SIJoZi+e35mjcUMfnRD8w/ouL0sTnxebT7xBCVucfRoMPA67USoChDpc+pNsdtsqlQOZMgpPZYfjIyCThv5mwjEKHnytBq46ULOFlHt0opplDANnDsvWwqEobhACZM+n2ZNtu36eoc3bC/Hak8ACEi5DixirF0w== miguel@MS90J8G8WL'
```

你现在可以使用此公钥来验证我生成的 token，并且你验证 token 不会给我带来任何安全风险。我仍然是世界上唯一能生成新 token 的人。

## 总结

我希望那些使用 JWT 和流行的 HS256 算法的人，现在准备去引入 RS256 或任何其他可用的公钥签名选项。

如果你有任何疑问，可以在评论区告诉我！