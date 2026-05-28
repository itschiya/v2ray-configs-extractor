import requests
import re

def scrape_configs():
    # آدرس فایل خام گیت‌هاب هدف
    url = "https://raw.githubusercontent.com/NiREvil/vless/main/README.md"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        
        # پیدا کردن کانفیگ‌های vless, vmess, trojan
        pattern = r'(?:vless|vmess|trojan)://[^\s<>"\'\n]+'
        configs = re.findall(pattern, content)
        
        # حذف موارد تکراری
        unique_configs = list(set(configs))
        
        # ذخیره در یک فایل متنی
        with open('configs.txt', 'w', encoding='utf-8') as f:
            for config in unique_configs:
                f.write(config + '\n')
                
        print(f"Successfully saved {len(unique_configs)} configs.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_configs()
