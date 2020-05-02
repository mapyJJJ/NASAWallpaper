#!/bin/bash
real_path=`ls -ll /usr/bin/nasa-wallpaper | awk '{print $11}'`
path=${real_path:0:-8}
start() { 
	PIDS=`ps -ef |grep 'NASAWallpaper' |grep -v grep | awk '{print $2}'`
	if [ "$PIDS" != "" ]; then
		echo "NASAWallpaper Server Already Start!"
	else
        /usr/bin/python3 $path/NASAWallpaper.py $second >/dev/null 2>&1 &
		if [[ "$?" -eq 0 ]];
		then
			echo "Server Start Success!"
		else
			echo "Server Start failure, please check"
		fi
	fi
}

stop() {
	PIDS=`ps -ef |grep 'NASAWallpaper' |grep -v grep | awk '{print $2}'`
	if [ "$PIDS" != "" ]; then
		kill -9 $PIDS
		if [[ "$?" -eq 0 ]];
		then
			echo "Server Stop Success!"
		else
			echo "Server Stop failure, please check!"
		fi
	else
		echo "Server not running"
	fi
}


restart() {
	PIDS=`ps -ef |grep 'NASAWallpaper' |grep -v grep | awk '{print $2}'`
	if [ "$PIDS" != "" ]; then
		echo "Waiting..."
        kill -9 $PIDS
        start
		if [[ "$?" -eq 0 ]];
		then
			echo "Server Restart Success!"
		else
			echo "Server Restart failure, please check!"
		fi
	else
		echo "Server Not Running ^_^"
		#执行启动
		start
	fi
}
if [ ! $2 ]; then
    if [ ! $1 = 'stop' ]; then
        echo "没有传入切换壁纸间隔时间"
        echo "Usage: $0 { start | stop | status } second"
        exit 1
    fi
else
    second=$2
fi

case "$1" in
'start')
	start
;;

'stop')
	stop
;;

'restart')
	restart
;;

*)
	echo "Usage: $0 { start | stop | status } min"
	exit 1
;;
esac
exit