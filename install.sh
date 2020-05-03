#!/bin/bash
if [ ! -f "/usr/bin/nasa-wallpaper" ]; then
    echo "创建软链接..."
    ln -s $(cd $(dirname $0); pwd)/start.sh /usr/bin/nasa-wallpaper
fi
echo "安装依赖..."
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ 
echo "安装完成"
echo "请新建terminal窗口, Usage: $0 { start | stop | status } min(切换壁纸间隔时间)"
