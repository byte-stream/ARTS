import os

""" GitBook 相关脚本"""


FOLDERS = ['Algorithm', 'Review', 'Tip', 'Share']


def generate_catalogue():
    """ 生成SUMMARY.md """
    text = '# Summary\n\n* [简介](README.md)\n'
    for folder in FOLDERS:
        text += '\n\n## {}\n\n'.format(folder)
        dirs = sorted(os.listdir(folder + '/'))[::-1]
        for d in dirs:
            text += '* [{}]()\n'.format(d)
            files = sorted(os.listdir(folder + '/' + d))
            for file in files:
                text += '    * [{}](./{}/{}/{})\n'.format(file, folder, d, file.replace(' ', '%20'))
        text += '\n\n---\n\n'
    with open('SUMMARY.md', 'wb') as file:
        file.write(text.encode('utf8'))


if __name__ == '__main__':
    generate_catalogue()
