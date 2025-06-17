
import os
import subprocess
from google.colab import files
import re

def clean_filename(input_string):
    # 使用正則表達式只保留字母和數字
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return cleaned_string

# 讀取使用者輸入的倉庫名稱和 image 名稱
repository = input("請輸入倉庫名稱：")
image_name = input("請輸入 image 名稱：")

target = repository + '/' + image_name
if target.startswith('/'):
  target = (image_name)

fileName =  clean_filename(image_name)

# 執行shell指令
subprocess.run(f"pip install udocker", shell=True, check=True)
subprocess.run(f"udocker --allow-root install", shell=True, check=True)
subprocess.run(f"udocker --allow-root pull --platform linux/amd64 {target}", shell=True, check=True)
subprocess.run(f"udocker --allow-root save --output /tmp/{fileName}.ima.tar {target}", shell=True, check=True)

# 下載生成的物件
files.download(f'/tmp/{fileName}.ima.tar')

# subprocess.run(f"rm /tmp/{fileName}.ima.tar", shell=True, check=True)

