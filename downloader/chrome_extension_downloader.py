import requests
import zipfile
import os
from google.colab import files
import json
import time
import random
from urllib.parse import quote

def get_extension_info(extension_id):
    """
    獲取擴展的基本信息
    """
    try:
        # 使用Chrome Web Store的API獲取擴展信息
        api_url = f"https://chrome.google.com/webstore/ajax/detail?id={extension_id}&hl=en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': f'https://chrome.google.com/webstore/detail/{extension_id}',
            'X-Same-Domain': '1'
        }
        
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            # 移除安全前綴
            content = response.text.replace(")]}'\n", "")
            data = json.loads(content)
            return data
        else:
            print(f"無法獲取擴展信息，狀態碼: {response.status_code}")
            return None
    except Exception as e:
        print(f"獲取擴展信息時發生錯誤: {e}")
        return None

def download_chrome_extension_v2(extension_id, extension_name=None):
    """
    改進版本的Chrome擴展下載器
    """
    print(f"正在嘗試下載擴展 ID: {extension_id}")
    
    # 嘗試多個不同的下載URL
    download_urls = [
        # 方法1: 使用update2 API
        f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=120.0.6099.129&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc",
        
        # 方法2: 使用不同的版本號
        f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=91.0.4472.124&acceptformat=crx3&x=id%3D{extension_id}%26uc",
        
        # 方法3: 使用webstore直接鏈接
        f"https://chrome.google.com/webstore/download/{extension_id}?hl=en&gl=US",
    ]
    
    # 設置更完整的請求頭
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }
    
    for i, url in enumerate(download_urls, 1):
        try:
            print(f"嘗試方法 {i}: {url[:60]}...")
            
            # 創建會話以保持cookie
            session = requests.Session()
            session.headers.update(headers)
            
            # 添加隨機延遲避免被檢測
            time.sleep(random.uniform(1, 3))
            
            # 發送請求
            response = session.get(url, stream=True, timeout=30, allow_redirects=True)
            
            print(f"響應狀態碼: {response.status_code}")
            print(f"響應頭Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"響應頭Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
            
            if response.status_code == 200:
                # 檢查內容類型
                content_type = response.headers.get('Content-Type', '').lower()
                if 'application' in content_type or 'octet-stream' in content_type:
                    # 確定文件名
                    if extension_name:
                        filename = f"{extension_name}_{extension_id}.crx"
                    else:
                        filename = f"extension_{extension_id}.crx"
                    
                    # 保存文件
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    file_size = os.path.getsize(filename)
                    print(f"文件大小: {file_size} bytes")
                    
                    if file_size > 0:
                        print(f"✓ 擴展下載成功: {filename}")
                        
                        # 驗證文件
                        if verify_crx_file(filename):
                            return filename
                        else:
                            print("⚠ 文件驗證失敗，嘗試下一個方法")
                            os.remove(filename)
                    else:
                        print("⚠ 下載的文件為空")
                        os.remove(filename)
                else:
                    print(f"⚠ 響應不是二進制文件，Content-Type: {content_type}")
            else:
                print(f"⚠ HTTP錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"⚠ 方法 {i} 失敗: {e}")
    
    print("✗ 所有下載方法都失敗了")
    return None

def verify_crx_file(filename):
    """
    驗證CRX文件是否有效
    """
    try:
        with open(filename, 'rb') as f:
            # 檢查CRX文件頭
            header = f.read(16)
            
            # CRX3 文件以 'Cr24' 開頭
            # CRX2 文件也以 'Cr24' 開頭
            if header[:4] == b'Cr24':
                print("✓ 檢測到有效的CRX文件頭")
                
                # 嘗試作為ZIP文件驗證
                try:
                    with zipfile.ZipFile(filename, 'r') as zip_file:
                        file_list = zip_file.namelist()
                        if 'manifest.json' in file_list:
                            print("✓ 文件驗證成功 - 包含manifest.json")
                            return True
                        else:
                            print("⚠ 警告: 未發現manifest.json文件")
                            return False
                except zipfile.BadZipFile:
                    print("⚠ 不是有效的ZIP格式，但可能是有效的CRX文件")
                    return True
            
            # 檢查是否是純ZIP文件
            elif header[:2] == b'PK':
                print("✓ 檢測到ZIP文件格式")
                with zipfile.ZipFile(filename, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    if 'manifest.json' in file_list:
                        print("✓ 文件驗證成功 - 包含manifest.json")
                        return True
                return False
            else:
                print(f"⚠ 未知文件格式，文件頭: {header[:8]}")
                return False
                
    except Exception as e:
        print(f"文件驗證失敗: {e}")
        return False

def download_via_third_party(extension_id):
    """
    通過第三方服務下載（備用方案）
    """
    print("嘗試通過第三方服務下載...")
    
    # 使用crxdl.com服務
    try:
        api_url = f"https://api.crxdl.com/download/{extension_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'download_url' in data:
                download_url = data['download_url']
                print(f"獲取到下載鏈接: {download_url}")
                
                # 下載文件
                file_response = requests.get(download_url, headers=headers, stream=True)
                if file_response.status_code == 200:
                    filename = f"extension_{extension_id}_third_party.crx"
                    with open(filename, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    if verify_crx_file(filename):
                        return filename
                    
    except Exception as e:
        print(f"第三方下載失敗: {e}")
    
    return None

def main_improved():
    """
    改進版主程序
    """
    print("Chrome擴展下載器 (改進版)")
    print("=" * 50)
    
    extension_id = input("請輸入Chrome擴展ID: ").strip()
    if not extension_id:
        print("錯誤: 擴展ID不能為空")
        return
    
    extension_name = input("請輸入擴展名稱 (可選): ").strip()
    
    # 首先獲取擴展信息
    print("\n正在獲取擴展信息...")
    ext_info = get_extension_info(extension_id)
    
    # 嘗試官方方法下載
    filename = download_chrome_extension_v2(extension_id, extension_name)
    
    # 如果官方方法失敗，嘗試第三方
    if not filename:
        print("\n官方下載失敗，嘗試第三方服務...")
        filename = download_via_third_party(extension_id)
    
    if filename:
        print(f"\n✓ 下載成功: {filename}")
        
        # 詢問是否下載到本地
        download_choice = input("\n是否下載文件到本地？(y/n): ").strip().lower()
        if download_choice == 'y':
            try:
                files.download(filename)
                print(f"文件 {filename} 已開始下載")
            except Exception as e:
                print(f"下載時發生錯誤: {e}")
    else:
        print("\n✗ 下載失敗")
        print("\n可能的解決方案:")
        print("1. 檢查擴展ID是否正確")
        print("2. 該擴展可能已下架或不可下載")
        print("3. 可能需要特殊權限或付費")
        print("4. 嘗試直接訪問Chrome Web Store手動下載")

# 運行改進版程序
if __name__ == "__main__":
    main_improved()
