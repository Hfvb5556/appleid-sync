import os
import re
import requests
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup

def download_image():
    """从目标网页获取图片"""
    url = "https://free.iosapp.icu"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据实际页面结构调整选择器
        img_tag = soup.find('img', {'alt': 'account-info'}) or soup.find('img', class_='account-img')
        if not img_tag:
            raise ValueError("未找到图片元素")
            
        img_url = img_tag['src']
        if img_url.startswith('/'):
            img_url = f"https://free.iosapp.icu{img_url}"
            
        img_data = requests.get(img_url, headers=headers).content
        with open('temp.jpg', 'wb') as f:
            f.write(img_data)
        return 'temp.jpg'
        
    except Exception as e:
        raise Exception(f"下载图片失败: {str(e)}")

def extract_account(image_path):
    """OCR识别账号密码"""
    try:
        # 图片预处理
        img = Image.open(image_path)
        img = img.convert('L')  # 灰度化
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        
        # 解析账号密码
        account = re.search(r'账号[:：]\s*([^\s@]+@[^\s]+)', text)
        password = re.search(r'密码[:：]\s*([^\s]+)', text)
        
        if not account or not password:
            raise ValueError("未识别到账号或密码")
            
        return account.group(1).strip(), password.group(1).strip()
        
    except Exception as e:
        raise Exception(f"OCR识别失败: {str(e)}")

if __name__ == '__main__':
    try:
        img_path = download_image()
        account, password = extract_account(img_path)
        
        with open('account.txt', 'w', encoding='utf-8') as f:
            f.write(f"账号: {account}\n密码: {password}")
            
        print("同步成功！")
        os.remove(img_path)  # 清理临时文件
        
    except Exception as e:
        print(f"错误: {str(e)}")
        exit(1)
