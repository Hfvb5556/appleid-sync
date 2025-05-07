import os
import re
import requests
from PIL import Image
import pytesseract

def download_image():
    """从目标网页下载图片"""
    url = "https://free.iosapp.icu"
    response = requests.get(url)
    # 这里需要根据实际网页结构调整选择器
    img_url = "https://free.iosapp.icu/path/to/image.jpg"  
    img_data = requests.get(img_url).content
    with open('temp.jpg', 'wb') as f:
        f.write(img_data)
    return 'temp.jpg'

def extract_account(image_path):
    """OCR识别账号密码"""
    text = pytesseract.image_to_string(Image.open(image_path), lang='chi_sim+eng')
    account = re.search(r'账号:\s*([^\s@]+@[^\s]+)', text).group(1)
    password = re.search(r'密码:\s*([^\s]+)', text).group(1)
    return account, password

if __name__ == '__main__':
    try:
        img_path = download_image()
        account, password = extract_account(img_path)
        with open('account.txt', 'w') as f:
            f.write(f"账号: {account}\n密码: {password}")
        print("同步成功！")
    except Exception as e:
        print(f"错误: {e}")
