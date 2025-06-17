# 引入所需的庫
import os
import re
import requests
import zipfile
from google.colab import files

def download_font(url, save_path):
    headers = { # 這裡使用一個常見的瀏覽器user-agent
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def process_css_file(css_file_path, fonts_dir):
    os.makedirs(fonts_dir, exist_ok=True)  # 確保目錄存在

    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()

    new_css_content = css_content
    font_urls = re.findall(r'src: url\((https://[^)]+)\) format', css_content)

    for url in font_urls:
        filename = url.split('/')[-1]
        save_path = os.path.join(fonts_dir, filename)
        download_font(url, save_path)
        new_css_content = new_css_content.replace(url, f'./fonts/google_fonts/{filename}')

    with open(css_file_path, 'w', encoding='utf-8') as file:
        file.write(new_css_content)

    return font_urls

# 設定檔案路徑和目錄
css_file_path = '/content/css/google-fonts.css'
fonts_dir = '/content/fonts/google_fonts'

# 創建 CSS 和 fonts 目錄
os.makedirs(os.path.dirname(css_file_path), exist_ok=True)
os.makedirs(fonts_dir, exist_ok=True)

# 假設 CSS 內容
css_content = """
# 裡面放google-fonts.css內容
"""
with open(css_file_path, 'w') as f:
    f.write(css_content)

# 呼叫函數處理 CSS
font_urls = process_css_file(css_file_path, fonts_dir)

# 壓縮下載的字型
zip_path = '/content/fonts.zip'
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, dirs, files_in_directory in os.walk(fonts_dir):
        for file in files_in_directory:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, os.path.join(fonts_dir, '..')))

# 提供下載
files.download(zip_path)
