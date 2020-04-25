import re
import os
import random
import requests
from datetime import datetime

image_dir = "/home/NASAWallpapers/images"
wallpaper_log_dir = "/home/NASAWallpapers/"

headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}

class SETWallpaper:
    def __init__(self) -> None:
        self.images = [m for m in os.listdir(image_dir) if m.split('.')[1] in ["jpg","png"]]
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
        try:
            with open(os.path.join(wallpaper_log_dir, "run.log"), 'r') as f:
                lines = f.readlines()
                last_image = lines[-1].split(">")[1].strip()
            if len(lines) > 100:
                # remove log file
                os.remove(os.path.join(wallpaper_log_dir, "run.log"))
        except:
            last_image = ''
        while True:
            image = random.choice(self.images)
            if image != last_image or not last_image:
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
        with open(os.path.join(wallpaper_log_dir, "run.log"), 'r') as f:
            lines = f.readlines()
            last_date = lines[-1].split(" ")[0]
        today_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if today_date == last_date:
            return
        self._download_pic(
            _text=self._get(self.iotd_page_url)
        )

class RecordLog:
    def __init__(self, image) -> None:
        self.wallpaper_log_path = wallpaper_log_dir
    def _record(self):
        if not os.path.exists(self.wallpaper_log_path):
            os.mkdir(self.wallpaper_log_path)
        with open(os.path.join(self.wallpaper_log_path, "run.log"), 'a') as f:
            f.write(f"{datetime.now()} set>{image}\n")

if __name__ == "__main__":
    NASAWallpaper()._main()
    image = SETWallpaper()._set()
    RecordLog(image)._record()