import os
import sys

"""
usage(python3):

python script.py 201902W3
"""

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
