# NASAWallpaper
## Linux采集NASA每日一图作为壁纸, 定时更换

### 目前支持的Linux桌面环境:

**gnome**
**预计适配xfce, KDE**


#### 前提环境配置: python3


## 使用说明:

#### 安装
```bash
./install.sh  # 安装
```

#### 开始使用
```bash
nasa-wallpaper start 60    # 开始(60s切换一次壁纸)
nasa-wallpaper restart 60
nasa-wallpaper stop
# 由于图片来自互联网，第一次使用等待几秒即可
```
#### 卸载
```bash
# 删除软链接
sudo rm /usr/bin/nasa-wallpaper
# 删除本地文件(图片， log文件)
sudo rm -rf ~/NASAWellpaper
```