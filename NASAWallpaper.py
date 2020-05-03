#!/usr/bin/python3
import re
import os
import sys
import time
import random
import requests
from datetime import datetime

image_dir = f"{os.environ['HOME']}/NASAWellpaper/images"
log_path = f"{os.environ['HOME']}/NASAWellpaper/run.log"

headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}

class SETWallpaper:
    def __init__(self) -> None:
        image_list = [m for m in os.listdir(image_dir) if m.split('.')[1] in ["jpg","png"]]
        self.images = image_list
    def _judge_env(self) -> str:
        desk_env = os.getenv("DESKTOP_SESSION")
        if "gnome" in desk_env:
            return "gnome"
        else:
            return "unkown desktop env"
    def _set(self):
        """ 
        judge desktop env to set
        remove file when over 100 lines
        random set NASA wallpaper
        """
        # judge desktop env
        desk_env = self._judge_env()
        last_images = []
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()
                for line in lines[-9:]:
                    last_images.append(line.split(">")[1].strip())
            if len(lines) > 100:
                # remove log file
                os.remove(log_path)
        except:
            pass
        while True:
            image = random.choice(self.images)
            if image not in last_images or not last_images:
                break
        image_path = os.path.join(image_dir, image)
        # set wallpaper
        if desk_env == "gnome":
            return_code = os.system(
                f"gsettings set org.gnome.desktop.background picture-uri 'file://{image_path}'"
            )
            if return_code == 0:
                return image
        else:
            return 'FAIL'

class NASAWallpaper:
    def __init__(self) -> None:
        self.iotd_page_url = "https://www.nasachina.cn/iotd"
        self.wallpaper_path = image_dir
    def _get(self, _url) -> str:
        req = requests.get(_url, headers=headers, timeout=5)
        if req.status_code == 200:
            return req.content
        return 'request error'
    def _download_pic(self, _text):
        p = r'src="([^"]*\.)(jpg|png)"'
        _res = re.findall(p, str(_text))
        try:
            if not os.path.exists(self.wallpaper_path):
                os.makedirs(self.wallpaper_path)
            for i,r in enumerate(_res):
                suffix = r[1]
                _url = '.'.join([re.findall(r'(.*)-\d*x\d*',r[0])[0], suffix])
                req = self._get(_url=_url)
                filename = f"NASAWallpaper-{datetime.now()}".split(" ")[0] + f"-{i}.{suffix}"
                file_path = os.path.join(self.wallpaper_path, filename)
                with open(file_path, 'wb') as f:
                    f.write(req)
        except Exception as e:
            print(e)
            return 'download error'
    def _main(self):
        today_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        # today_date = '2020-05-04'
        with open(log_path, 'r') as f:
            lines = f.readlines()
            if lines:
                last_date = lines[-1].split(" ")[0]
                if today_date == last_date:
                    return
            image_list = [m for m in os.listdir(image_dir) if m.split('.')[1] in ["jpg","png"]]
            for image in image_list:
                date = '-'.join(image.split("-")[1:4])
                if date != today_date:
                    os.remove(os.path.join(image_dir, image))
            self._download_pic(
                _text=self._get(self.iotd_page_url)
            )

class RecordLog:
    def __init__(self, image) -> None:
        self.image = image
    def _record(self):
        with open(log_path, 'a') as f:
            f.write(f"{datetime.now()} set>{self.image}\n")

def gen_dir():
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.isfile(log_path):
        os.mknod(log_path)

try:
    cicle_time = int(sys.argv[1])
    print(cicle_time)
    while True:
        gen_dir()
        NASAWallpaper()._main()
        image = SETWallpaper()._set()
        RecordLog(image)._record()
        time.sleep(cicle_time)
except Exception as e:
    print(e)
    sys.exit(0)