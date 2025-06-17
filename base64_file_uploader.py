######### Python 檔案轉Base64
import base64
from tkinter import Tk, filedialog

def encode_file_to_base64(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        file_content = file.read()
    
    base64_encoded_content = base64.b64encode(file_content).decode('utf-8')
    
    with open(output_file_path, 'w') as file:
        file.write(base64_encoded_content)

def main():
    # Initialize Tkinter root
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select the input file
    input_file_path = filedialog.askopenfilename(title="Select a file to encode")
    if not input_file_path:
        print("No file selected. Exiting.")
        return

    # Open file dialog to select the output file path
    output_file_path = filedialog.asksaveasfilename(
        title="Select the destination file", defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not output_file_path:
        print("No output file selected. Exiting.")
        return

    # Encode the file content and save to the output file
    encode_file_to_base64(input_file_path, output_file_path)
    print(f"File has been encoded and saved to {output_file_path}")

if __name__ == "__main__":
    main()


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
