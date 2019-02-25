## ARTS周报脚本

因为每周都需要`寒食君`手动整理周报，所以小弟用python简单写了下我们ARTS周报的脚本。

> 为图方便，所以写的很简陋，欢迎提PR修改这个`low script`

使用方法就是ARTS目录下，bash下执行  

```bash
python script.py 201902W3  # 指定周
```

具体代码如下

```python
import os
import sys


folders = ['Algorithm', 'Review', 'Share', 'Tip']


def write_by_utf8(obj, args):
    obj.write(args.encode('utf8'))


def main(week: str):
    length = len(os.listdir('./Weekly/'))
    if week not in os.listdir('./Weekly')[-1]:
        length += 1
    with open('./Weekly/' + week + '.md', 'wb') as md:
        write_by_utf8(md, '# Weekly #{}\n\n'.format(length))
        write_by_utf8(md, '这是ARTS计划的第*{}*周，一共有*{}*位同学完成了目标\n\n'.format(length, '(占坑)'))
        for folder in folders:
            write_by_utf8(md, '## {}\n\n'.format(folder))
            if folder == 'Algorithm':
                write_by_utf8(md, '[这里](../Algorithm/{})\n\n'.format(week))
                continue
            files = os.listdir(folder + '/' + max(os.listdir(folder)))
            for file in files:
                write_by_utf8(md, '[{}](../{}/{}/{})\n\n'.format(file[:-3], folder, week, file.replace(' ', '%20')))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
```

