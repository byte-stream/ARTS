#!/usr/bin/env bash

#  创建gh-pages分支
branch=$(git branch | grep gh-pages)
if [ -n "$branch" ]; then
    git br -D gh-pages
fi

git co -b gh-pages

# book.json
cat>book.json<<EOF
{
    "plugins": [
        "expandable-chapters-small",
        "search",
        "splitter"
        ]
}
EOF

# 生成目录文件
python script/catalogue.py

# 生成book HTML
gitbook install ./ && gitbook build

git rm --cached -r . && git clean -df

cat>./.gitignore<<EOF
.idea/
__pycache__/
_book/
EOF

cp -r _book/* . && rm -rf _book/

git add . && git commit -m 'publish book'

echo "Build book down!，next,  git push .."