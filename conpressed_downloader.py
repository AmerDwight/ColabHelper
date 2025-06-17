import requests
import zipfile
from io import BytesIO
from google.colab import files

# 輸入檔案URL
file_url = input("請輸入檔案URL：")

# 下載檔案內容
response = requests.get(file_url)
file_content = response.content

# 壓縮檔案
with zipfile.ZipFile('compressed.zip', 'w') as zipf:
    zipf.writestr(file_url.split('/')[-1], file_content)

# 下載壓縮檔案
files.download('compressed.zip')
