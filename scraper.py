import requests
import re
import base64
import random
from concurrent.futures import ThreadPoolExecutor

def extract_configs(text):
    configs = []
    # تلاش برای دیکد کردن Base64
    try:
        clean_text = text.strip()
        padding = len(clean_text) % 4
        if padding != 0:
            clean_text += '=' * (4 - padding)
        decoded_bytes = base64.b64decode(clean_text)
        text_to_search = decoded_bytes.decode('utf-8', errors='ignore')
    except Exception:
        text_to_search = text
        
    # الگوی پیدا کردن انواع کانفیگ‌ها
    pattern = r'(?:vless|vmess|trojan|ss|tuic|hy2|wireguard)://[^\s<>"\'\n]+'
    return re.findall(pattern, text_to_search)

def fetch_and_extract(url):
    try:
        # فیلتر کردن تگ‌های اضافی مثل [AS?] از انتهای لینک
        clean_url = url.split(' ')[0].strip()
        if not clean_url.startswith('http'):
            return []
            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(clean_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            configs = extract_configs(response.text)
            configs.extend(re.findall(r'(?:vless|vmess|trojan|ss|tuic|hy2|wireguard)://[^\s<>"\'\n]+', response.text))
            return list(set(configs))
    except:
        pass
    return []

def main():
    print("در حال خواندن لیست منابع از sources.txt ...")
    
    # 1. خواندن لیست لینک‌ها از فایل sources.txt
    sub_links = []
    try:
        with open('sources.txt', 'r', encoding='utf-8') as f:
            for line in f:
                # اگر خط خالی نبود و با http شروع میشد
                clean_line = line.strip()
                if clean_line.startswith('http'):
                    # حذف تگ‌های اضافی
                    url = clean_line.split(' ')[0]
                    sub_links.append(url)
    except Exception as e:
        print(f"خطا در خواندن sources.txt: {e}")
        return

    print(f"{len(sub_links)} لینک سابسکریپشن پیدا شد. در حال استخراج کانفیگ‌ها...")
    
    # 2. بررسی همزمان سایت‌ها
    all_configs = set()
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_and_extract, sub_links)
        for configs in results:
            all_configs.update(configs)
            
    if not all_configs:
        print("\nهیچ کانفیگی پیدا نشد!")
        return

    # تبدیل set به لیست برای انجام عملیات
    config_list = list(all_configs)
    
    print(f"\nمجموعا {len(config_list)} کانفیگ استخراج شد.")
    
    # 3. محدود کردن خروجی به 50 کانفیگ
    # برای تنوع، لیست رو به هم می‌ریزیم تا هر بار 50 کانفیگ مختلف انتخاب بشه
    random.shuffle(config_list)
    final_configs = config_list[:50]
    
    print(f"تعداد {len(final_configs)} کانفیگ نهایی برای ذخیره انتخاب شد.")
    
    # 4. ذخیره مستقیم در فایل configs.txt برای گیت‌هاب اکشن
    with open('configs.txt', 'w', encoding='utf-8') as f:
        for c in final_configs:
            f.write(c + '\n')
            
    print("فایل configs.txt آپدیت شد.")

if __name__ == "__main__":
    main()
