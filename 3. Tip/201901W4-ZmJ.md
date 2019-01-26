## Git  Hook 自定义工作流

Git 中提供了一些钩子，可以在特定事件发生时，触发运行准备好的钩子脚本（语言不限），钩子文件在初始化仓库时，就存在于`.git/hooks`路径下，只不过被标上`.simple`而不会执行，每个钩子根据命名都有不用的使用场景。

如果想使用钩子，只需要简单的几步即可，重要的还是脚本的准备，这里以`pre-commit`为例。

移动到项目下
```bash
cd <project path>
```

将准备好的脚本放入hooks中，当然也可以直接`vim pre-commit`

```bash
cp <script file>  .git/hooks/pre-commit
```

最后需要给脚本提供执行权限
```bash
chmod u+x .git/hooks/pre-commit
```
---

最后分享下自己正在使用的`pre-commit`，在`git commit` 时，触发脚本检查代码规范。

```shell
set -e

# get changed (modified + staged) python files
PYTHON_FILES="`git diff --name-only --diff-filter=AM HEAD | grep --color=never '.py$' || true`"

# do nothing if no python file
if [ ! "${PYTHON_FILES}" ]; then
  exit 0
fi

echo 'Running flake8...'
pipenv run flake8 ${PYTHON_FILES}

PYLINT_FILES="`git diff --name-only --diff-filter=AM HEAD | grep --color=never '.py$' | grep -v migrations || true`"

# do nothing if no python file
if [ ! "${PYLINT_FILES}" ]; then
  exit 0
fi

echo 'Running pylint...'
pipenv run pylint ${PYLINT_FILES}

exit 0
```



> 具体可以查看这篇<a href='https://github.com/geeeeeeeeek/git-recipes/wiki/5.4-Git-%E9%92%A9%E5%AD%90%EF%BC%9A%E8%87%AA%E5%AE%9A%E4%B9%89%E4%BD%A0%E7%9A%84%E5%B7%A5%E4%BD%9C%E6%B5%81'>wiki</a>
