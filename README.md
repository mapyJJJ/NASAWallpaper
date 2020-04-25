# NASAWallpaper
## Linux采集NASA每日一图作为壁纸, 定时更换

### 支持的Linux桌面环境:

**gnome**

**xfce**

## 环境配置: python3, crontab
> pip3 install -r requirements.txt

> apt-get install crontab -y

> yum install crontab -y

## 使用说明:
> python3 NASAWallpapaer.py  # 直接运行看效果

### 搭配crontab使用
> crontab -e #进入编辑模式

> \*/15 * * * * python3 NASAWallpaper.py  # 每15min更换一次壁纸