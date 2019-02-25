# 在 PyCharm 中设置 Flask 程序

** 本文为翻译 **

**原文地址: https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-pycharm**

在这篇短文和视频中, 我想给你一些关于在 PyCharm 中设置 Flask 程序的技巧。 我们的想法是在 PyCharm 社区版 中设置 Flask 程序, 以便执行、调试和测试。 这是一个非常棒的 IDE, 可以完全免费下载和使用。
如果你想看我的具体操作, 请看下面的视频。 然后, 如果你想要快速参考和所需步骤的摘要, 可以回过头来看这篇文章。
[https://www.youtube.com/watch?time_continue=134&v=bZUokrYanFM](https://www.youtube.com/watch?time_continue=134&v=bZUokrYanFM "视频链接")

## 在 PyCharm 中创建一个 Flask 项目

这一节非常简单。 你需要做的是启动 PyCharm, 选择 `Open`, 然后选择你项目所在的目录。 Pycharm 将会创建一个新的项目并打开它。 左边的侧边栏将显示一个包含项目中所有文件的目录树.

## 在配置中添加运行和调试

你想要做的第一件事可能就是运行你的项目。 PyCharm 使用 "配置" 的概念, "配置" 是定义运行或调试任务的参数集。 为了创建或修改配置, 你必须在菜单中勾选 **Run|Edit Configurations**..., 如果这个操作被禁用, 你只需要等一下, 让 PyCharm 完成项目的初始后台解析。

为了创建一个新的配置, 点击 **+** 号, 并且勾选 **Python**. 在名称字段这, 输入配置的说明, 例如 "webapp". 我通常会勾选 **Single Instance Only** 选项, 因为对于 web 程序, 运行多个实例并不是非常有用。

在 **Script path** 你需要选择 **flask** 工具, 它是在 **bin** 目录下的虚拟环境。 在这里你可以使用 `...`按钮去浏览并且勾选脚本。 如果你想在你的项目外保存虚拟环境, 或者如果你使用虚拟环境增强版(environment wrapper 虚拟环境包装器??)如 pipenv, 它有自己的 virtualenvs 位置, 你需要找出 virtualenv 所在的位置并浏览到该目录, 然后进入到 bin 目录下找到 flask 命令. 如果你的虚拟环境目录跟你项目目录一样, 那么就会方便得多。 在 Windows 上查找 **Scripts** 子目录, 并且在目录下查找 **flask.exe** 并勾选。

在 **Parameters** 字段中输入你需要执行的命令。 这与上一个操作想结合来执行我们熟悉的 **flask run** 命令。

我相信你也记得, flask 命令需要一个 `FLASK_APP` 环境变量去指向你的 Flask 程序。 这个变量需要在 **Environment variables**中定义。变量与你在命令行中运行的程序名一样, 如果你想在你的项目中使用 **.flaskenv** 文件, 那么你已完成了配置, 将从哪里导入环境变量。

最后不同的是, 你需要去设置 **Working directory **去指向你的项目目录, 而不是 flask 命令指向的目录。

现在你可以关闭配置的窗口了. PyCharm 窗口右上角是刚刚添加的配置. 如果你点击绿色的 "run" 按钮, 你的项目应该会启动, 或者你可以点击 "bug" 按钮将会在 "debugger" 模式下启动. 使用调试器非常有用, 因为你可以打断点来停止程序执行, 并检查变量或逐步运行程序的一部分.

## 运行单元测试

除了能够运行和调试你的程序, 对 PyCharm 跑单元测试也非常有用。 这需要将第二个配置添加到项目中. 那么回到 **Run|Edit Configurations** 菜单选项中, 并且再次点击 **+**号去创建一个新的配置. 这次选择 **Python tests** 配置类型, 然后选择你想要使用的测试运行器. 在视频演示中, 我选择了 **Unittests**, 它是基于在 Python 的 unittest 包.

将配置名称设置为类似于 tests。在**Target** 字段中确保选择 **Script path**, 然后单击右侧的 **...** 按年选择 tests 所在的目录。 在 **Pattern** 字段中, 输入适用于包含 tests 的所有模块的文件模式。 一些常见的模式是 test_*.py, *_test.py *test*.py. 为了完成这个测试配置, 在 **Working directory** 字段中选择你的项目目录。

在你关掉配置窗口后, PyCharm 窗口右上角选择 tests. 如果你需要 **webapp** 配置, 那么你可以回到这个配置。 选择 tests 后, 你可以单击绿色的 run 按钮来运行单元测试。 PyCharm 检测到你正在运行的测试, 窗口底部的面板向你显示了测试的执行情况。 将会显示任何失败的测试, 如果你单击每个测试, 你可以看到它的输出。 还可以通过单击绿色的 debugger 按钮在调试器下运行, 这样你就可以逐步打断点来调试指定的部分了。

PyCharm 还在侧边栏上添加了一个小的运行按钮, 在每个单元测试功能或方法旁边, 这非常方便, 因为它允许你通过单击按钮来运行或调试单个测试。

## 增强 Debug 配置

如果你到了这一步, 你的项目配置已经很不错了, 但还有一个细节缺失了。当你的 Flask 程序崩溃, 你知道有两种可能的结果。 如果未启用调试模式, 则客户端将收到 500 的状态码, 如果启用了调试器, 则会引入基于浏览器的调试器。当你在 PyCharm 调试器下运行程序时, 如果崩溃会在断点这停止程序, 那么你可以检查变量并找出错误的地方。不幸的是, 由于 Flask 中已存在很长时间的错误, 如果你按照上面的说明配置 PyCharm 项目, 这将不起作用。更具体地说, 这是一个影响使用 flask run 命令启动的 Flask 程序的错误, 但适用于运行 app.run() 方法。 

如果你想在程序崩溃时, 利用 PyCharm 调试器, 你必须切换到 app.run(). 首先, 确保你的程序的主脚本(通常是你在FLASK_APP环境变量中设置的脚本)在底部具有此脚本:

```
if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
```

这创建了另一个启动 Flask 程序的方法, 你可以在需要的时候使用它， 不需要运行 app.run() 命令。 我添加的 app.run() 调用调试模式, 单关闭调试器和重新加载器, 以便它们不会干扰 PyCharm。 `passthrough_errors` 选项是使 PyCharm 崩溃的关键, 不幸的是, 当你通过 flask run 运行程序时, 无法设置此选项。

下一个更改是修改 PyCharm 中的运行配置, 并通过 app.run() 调用启动程序。 选择 PyCharm 窗口右上角的 webapp 配置, 并回到 **Run|Edit Configurations....**中, 修改 **Script path** 去指向你的主脚本, 即现在 app.run()这个脚本。 **Parameters** 必须为空, 因此在启动前清空它. 使用 app.run() 时不需要设置 `FLASK_APP` 环境变量, 因此你可以从配置中删除它, 尽管它不会影响任何东西。

如果你现在启动程序, 异常触发的崩溃都被 PyCharm 捕获, 这将停止程序并显示崩溃的文章, 交互式堆栈跟踪以及坚持变量值的功能。

## 总结

我希望这是开始使用 PyCharm 的指南。在以后的文章中, 我将使用 Visual Studio Code 进行相同的联系, 这是另一个非常好的 Python IDE. 使用 PyCharm 时, 你还有其他任何犹豫的设置步骤吗? 请在以下评论中告诉我!