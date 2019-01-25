# 《Flask Web 开发实战》 之 Flask 的工作流程与机制
> 本节我们会深入到 Flask 的源码来了解请求、响应、路由处理等功能是如何实现的。

## Flask 中的请求响应循环

**1. 程序启动**

目前我们有两种方法启动开发服务器, 一种是在命令行中使用 `flask
run` 命令（会调用 `flask.cli.run_command()`函数)，另一种是使用被弃用的 `flask.Flask.run()`方法。不论是 `run_command()`函数，还是以前用于运行程序的 run() 函数，它们都在最后调用了werkzeug.serving 模块中的 `run_simple()` 函数

```
def run_simple(hostname, port, application, use_reloader=False,
               use_debugger=False, use_evalex=True,
               extra_files=None, reloader_interval=1,
               reloader_type='auto', threaded=False,
               processes=1, request_handler=None, static_files=None,
               passthrough_errors=False, ssl_context=None):
    if use_debugger:
    	from werkzeug.debug import DebuggedApplication
	application = DebuggedApplication(application, use_evalex)
    if static_files:
	from werkzeug.wsgi import SharedDataMiddleware
	application = SharedDataMiddleware(application, static_files)
	...
        def inner():
	    try:
		fd = int(os.environ['WERKZEUG_SERVER_FD'])
		except(LookupError, ValueError):
			fd = None
		srv = make_server(hostname, port, application, threaded,
                          processes, request_handler,
                          passthrough_errors, ssl_context,fd=fd)
	        if fd is None:
	            log_startup(srv.socket)
	        srv.serve_forever()
		    if use_reloader:
		    ...
		    	from werkzeug._reloader import run_with_reloader
        	    	run_with_reloader(inner, extra_files, reloader_interval, reloader_type)
		    else:
		        inner()
```

   在这里使用了两个 Werkzeug 提供的中间件，如果 use_debugger 为
Ture, 也就是开启调试模式, 那么就使用 DebuggedApplication 中间件为
程序添加调试功能。 如果 static_files 为 True, 就使用
SharedDataMiddleware 中间件为程序添加提供 (serve) 静态文件的功能。

这个方法最终会调用 inner() 函数，函数中的代码和我们在上一节
创建的 WSGI 程序末尾很像。它使用 make_server() 方法创建服务器，
然后调用 serve_forever() 方法运行服务器。为了避免偏离重点，中间
在 Werkzeug 和其他模块的调用我们不再分析。我们在前面学习过 WSGI
 的内容，当接收到请求时，WSGI 服务器会调用 Web 程序中提供的可调
用对象，这个对象就是我们的程序实例 app。现在，第一个请求进入
了。

**2.请求In**

Flask 类实现了__call__() 方法，当程序实例被调用时会执行这个
方法, 而这个方法内部调用了 Flask.wsgi_app（）方法。

```
class Flask(_PackageBoundObject):
    ...
    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
```

通过 `wsgi_app()` 方法接收的参数可以看出来, 这个 wsgi_app()
方法就是隐藏在 Flask 中的那个 WSGI 程序。 这里将 WSGI 程序实现在单
独的方法中, 而不是直接实现在 __call__() 方法中, 主要是为了在方
便附加中间件的同时保留对程序实例的引用。

wsgi_app() 方法中的 try...except... 语句是重点。它首先尝试从
`Flask.full_dispatch_request()` 方法获取响应，如果出错那么就根据错误
类型来生成错误响应。我们来看看处理请求并生成响应的
Flask.full_dispatch_request() 方法, 它负责完整地请求调度（full
request dispatching）

```
class Flask(_PackageBoundObject):
    def full_dispatch_request(self):
	"""分发请求, 并对请求进行预处理和后处理。同时捕捉 HTTP 异常并处理错误
	"""
	self.try_trigger_before_first_request_functions()
	try:
	    request_started.send(self) # 发送请求进入信号
	    rv = self.preprocess_request() # 预处理请求
	    if rv is None:
	        rv = self.dispatch_request() # 进一步处理请求，获取返回值
        except Exception as e:
            rv = self.handle_user_exception(e) # 处理异常
        return self.finalize_request(rv) # 最终处理
```

在这个函数中调用了 preprocess_request() 方法对请求进行预处理
(request preprocessing), 这会执行所有使用 `before_request` 钩子注册的函数。

接着, 请求分发的工作会进一步交给 `dispatch_request() `方法, 它
会匹配并调用对应的视图函数, 获取其返回值, 在这里赋值给 rv, 请求
调度的具体细节我们会在后面了解。 最后, 接收视图函数返回值的
finalize_request() 会使用这个值来生成响应。

**3.响应out**

接收到视图函数返回值的 finalize_request() 函数负责生成响应,
即请求的最终处理

```
class Flask(_PackageBoundObject):
    def finalize_request(self, rv, from_error_handler=False):
    """把视图函数返回值转换为响应，然后调用后处理函数。
    """
        response = self.make_response(rv) # 生成响应对象
        try:
            response = self.process_response(response) # 响应预处理
            request_finished.send(self, response=response) # 发送信号
        except Exception:
            if not from_error_handler:
                raise
	    self.logger.exception('Request finalizing failed with an error while handling an error')
	return response
```

这里使用 Flask 类中的 make_response() 方法生成响应对象, 但这
个 make_response 并不是我们从 flask 导入并在视图函数中生成响应对象的 make_response, 我们平时使用的 make_response 是 helpers 模块中的 make_response() 函数, 它对传入的参数进行简单处理, 然后把参数传递给 Flask 类的 make_response 方法并返回。后面我们会详细了解响应对象。

除了创建响应对象，这段代码主要调用 process_response () 方法处理响应。 这个响应处理方法会在把响应发送给 WSGI 服务器前执行所有使用 after_request 钩子注册的函数。另外, 这个方法还会根据 session 对象来设置cookie, 后面我们会详细了解。

返回作为响应的 response 后, 代码执行流程就回到了 wsgi_app()
方法, 最后返回响应对象, WSGI 服务器接收这个响应对象, 并把它转
换成HTTP响应报文发送给客户端。


