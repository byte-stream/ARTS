import os
import re
import sys

from collections import Counter
from urllib import request

"""
usage(python3):

pip install requests
python weekly.py 201902W3
"""

folders = ['Algorithm', 'Review', 'Tip', 'Share']


def write_by_utf8(obj, text: str):
    obj.write(text.encode('utf8'))


def get_name(filename: str) -> str:
    """ 获取文件作者名"""
    return filename.split('-')[-1][:-3]


def get_achieve_goal_authors(week: str) -> list:
    """ 获取完成ARTS的作者名 """
    folders_authors = []
    for folder in folders:
        folder_authors = map(get_name, os.listdir(folder + '/' + week))
        folders_authors.extend(folder_authors)
    author_counts = Counter(folders_authors)  # 每个作者达成的个数
    achieve_authors = [name for name, count in author_counts.items() if int(count) > 3]  # 完成目标的作者
    return achieve_authors


def generate_image(size='1200x800', image_type='books,nature') -> str:
    """
    随机抓取一张unsplash的图片
    https://source.unsplash.com/
    """
    url = 'https://source.unsplash.com/{size}/?{type}'.format(size=size, type=image_type)
    try:
        image_url = request.urlopen(url, timeout=4).url
    except request.URLError:
        print('Fetch image timeout, Retry or add images manually!')
        image_url = ''
    return image_url


def generate_partners(length, week: str) -> str:
    """ 生成Partners模块"""
    achieve_authors = get_achieve_goal_authors(week)
    text = '这是ARTS计划的第*{}*周，一共有*{}*位同学完成了目标\n\n'.format(length, len(achieve_authors))
    text += '## Partners\n\n'
    for author in achieve_authors:
        if author + '.md' in os.listdir('./Partners'):
            text += '[@{}](../{}/{})\n\n'.format(author, 'Partners', author+'.md')
        else:
            text += '@{}\n\n'.format(author)
    return text


def generate_folders(week: str) -> str:
    """ 生成ARTS模块"""
    text = ''
    for folder in folders:
        text += '## {}\n\n'.format(folder)
        if folder == 'Algorithm':
            text += '[这里](../Algorithm/{})\n\n'.format(week)
            continue
        files = os.listdir(folder + '/' + week)
        for file in files:
            text += '[{}](../{}/{}/{})\n\n'.format(file[:-3], folder, week, file.replace(' ', '%20'))
    return text


def generate_weekly_collect():
    """ 生成汇总 """
    text = '\n\n'
    for i, file in enumerate(sorted(os.listdir('Weekly'))):
        text += '[第{}周](/Weekly/{})\n'.format(i+1, file)
    text += '\n\n'
    with open('./README.md', 'rb') as md:
        content = md.read().decode('utf8')
    left = content.find('## 汇总') + len('## 汇总')
    right = content.find('## 联系')
    content = content[:left] + text + content[right:]
    with open('./README.md', 'wb') as md:
        write_by_utf8(md, content)
    return text


def main(week: str):
    length = len(os.listdir('./Weekly/'))
    if week + '.md' not in os.listdir('./Weekly'):
        length += 1
    image_url = generate_image()
    partners_text = generate_partners(length, week)
    arts_text = generate_folders(week)
    with open('./Weekly/' + week + '.md', 'wb') as md:
        write_by_utf8(md, '# Weekly #{}\n\n'.format(length))
        write_by_utf8(md, '![]({})\n\n'.format(image_url))
        write_by_utf8(md, partners_text)
        write_by_utf8(md, arts_text)
    generate_weekly_collect()


def check_filename():
    for folder in folders:
        dirs = os.listdir(folder + '/')
        for d in dirs:
            files = os.listdir(folder + '/' + d)
            for file in files:
                if ' ' in file:
                    raise Exception('文件名中请用(-)替换空格 {}/{}/{}'.format(folder, d, file))
                if not re.match(r'.*-(.*)\.md', file):
                    raise Exception('文件名不规范 {}/{}/{}'.format(folder, d, file))
    return 'success'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        check_filename()
