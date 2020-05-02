#!/bin/bash
touch $(cd $(dirname $0); pwd)/start.pid
echo $(cd $(dirname $0); pwd)/NASAWallpaper.py > record.txt
for line in `cat $(cd $(dirname $0); pwd)/start.pid`
do
    echo $line
    kill -9 $line
done
nohup python3 $(cd $(dirname $0); pwd)/NASAWallpaper.py 0.1 >/dev/null 2>&1 & echo $! > $(cd $(dirname $0); pwd)/start.pid