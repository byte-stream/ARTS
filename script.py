import os
import sys

"""
usage:
    shell: python script.py 201902W1
"""

folders = ['Algorithm', 'Review', 'Share', 'Tip']


def main(week: str):
    length = len(os.listdir('./Weekly/'))
    if week not in os.listdir('./Weekly')[-1]:
        length += 1
    with open('./Weekly/' + week + '.md', 'wb') as md:
        md.write('# Weekly #{}\n\n'.format(length).encode('utf8'))
        md.write('这是ARTS计划的第*{}*周，一共有*{}*位同学完成了目标\n\n'.format(length, '(占坑)').encode('utf8'))
        for folder in folders:
            md.write('## {}\n\n'.format(folder).encode('utf8'))
            if folder == 'Algorithm':
                md.write('[这里](../Algorithm/{})\n\n'.format(week).encode('utf8'))
                continue
            files = os.listdir(folder + '/' + max(os.listdir(folder)))
            for file in files:
                if '-name' in file:
                    continue
                md.write('[{}](../{}/{}/{})\n\n'.format(
                    file[:-3], folder, week, file.replace(' ', '%20')).encode('utf8'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
