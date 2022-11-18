#!/bin/bash

tag=2
page=21
wget https://raw.githubusercontent.com/dwuggh/prler/master/main.py
pacman -S python-beautifulsoup4
echo $tag > tag
nohup python main.py $tag $page $
