######### COLAB Base6轉換成檔案，儲存於google drive根目錄
import base64
from google.colab import drive

# 掛載 Google Drive
drive.mount('/content/drive')

# 輸入 Base64 編碼的資料
base64_data = input("請輸入 Base64 編碼的資料：")

# 輸入檔案名稱及副檔名
file_name = input("請輸入檔案名稱（包含副檔名）：")

# 將 Base64 編碼的資料解碼並寫入檔案
decoded_data = base64.b64decode(base64_data)

# 設定檔案儲存路徑
file_path = f"/content/drive/My Drive/{file_name}"

# 將解碼後的資料寫入檔案
with open(file_path, 'wb') as file:
    file.write(decoded_data)

print(f"檔案已成功儲存到 Google Drive：{file_path}")
