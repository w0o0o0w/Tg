# tg.py
# =================================================================
# 🚀 کد کامل وب‌سرویس TGJU - استخراج ارز، طلا و سکه
# =================================================================
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

class TGJUCompleteAPI:
    """
    وب‌سرویس کامل برای استخراج قیمت ارز، طلا و سکه از TGJU.org
    
    ویژگی‌ها:
    ✅ استخراج ۳۴ ارز مختلف (ارزهای اصلی، منطقه‌ای و رمزارزها)
    ✅ استخراج ۱۵ نوع طلا (طلای خالص، مثقال، صندوق‌های طلا)
    ✅ استخراج ۱۹ نوع سکه (سکه‌های اصلی و حباب‌ها)
    ✅ پشتیبانی از JSON export
    ✅ جستجوی آیتم‌های خاص
    ✅ خروجی استاندارد با timestamp
    """
    
    def __init__(self):
        self.base_url = "https://www.tgju.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_all_data(self):
        """استخراج تمام داده‌ها از TGJU"""
        try:
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ایجاد دیکشنری‌های نتیجه
            currencies = {}
            gold_data = {}
            coins_data = {}
            
            # جستجو در تمام جداول صفحه
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 6:
                        cell_texts = [cell.get_text(strip=True) for cell in cells]
                        
                        if cell_texts[0] and cell_texts[1]:
                            item_name = cell_texts[0]
                            category = self.categorize_item(item_name)
                            
                            if category:
                                item_data = {
                                    'name': item_name,
                                    'price': cell_texts[1],
                                    'change': cell_texts[2] if len(cell_texts) > 2 else '',
                                    'min_price': cell_texts[3] if len(cell_texts) > 3 else '',
                                    'max_price': cell_texts[4] if len(cell_texts) > 4 else '',
                                    'time': cell_texts[5] if len(cell_texts) > 5 else '',
                                    'timestamp': datetime.now().isoformat(),
                                    'category': category
                                }
                                
                                key = self.create_key(item_name)
                                
                                if category == 'currency':
                                    currencies[key] = item_data
                                elif category == 'gold':
                                    gold_data[key] = item_data
                                elif category == 'coin':
                                    coins_data[key] = item_data
            
            return {
                'status': 'success',
                'summary': {
                    'total_currencies': len(currencies),
                    'total_gold': len(gold_data),
                    'total_coins': len(coins_data),
                    'total_items': len(currencies) + len(gold_data) + len(coins_data)
                },
                'data': {
                    'currencies': currencies,
                    'gold': gold_data,
                    'coins': coins_data
                },
                'source': 'TGJU.org',
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'خطا در استخراج: {str(e)}'
            }
    
    def categorize_item(self, item_name):
        """تشخیص نوع آیتم بر اساس نام"""
        item_lower = item_name.lower()
        
        # کلمات کلیدی ارزها
        currency_keywords = [
            'دلار', 'یورو', 'پوند', 'درهم', 'یوان', 'ین', 'کرون', 'لیر', 
            'دینار', 'روپیه', 'فرانک', 'رینگیت', 'بیت کوین', 'لایت کوین',
            'دوج کوین', 'بایننس', 'شیبا', 'تون', 'پلاتین'
        ]
        
        # کلمات کلیدی طلا
        gold_keywords = ['طلا', 'gold', 'مثقال', 'انس طلا', 'صندوق طلا']
        
        # کلمات کلیدی سکه
        coin_keywords = ['سکه', 'حباب', 'تمام سکه']
        
        if any(keyword in item_lower for keyword in currency_keywords):
            return 'currency'
        elif any(keyword in item_lower for keyword in gold_keywords):
            return 'gold'
        elif any(keyword in item_lower for keyword in coin_keywords):
            return 'coin'
        
        return None
    
    def create_key(self, name):
        """ایجاد کلید منحصر به فرد از نام فارسی"""
        key = re.sub(r'[^\w\s]', '', name)
        key = re.sub(r'\s+', '_', key.strip())
        return key.lower()
    
    def get_currencies_only(self):
        """فقط ارزها را برگردان"""
        data = self.extract_all_data()
        if data['status'] == 'success':
            return {
                'status': 'success',
                'count': data['summary']['total_currencies'],
                'currencies': data['data']['currencies'],
                'last_updated': data['last_updated']
            }
        return data
    
    def get_gold_only(self):
        """فقط طلا را برگردان"""
        data = self.extract_all_data()
        if data['status'] == 'success':
            return {
                'status': 'success',
                'count': data['summary']['total_gold'],
                'gold': data['data']['gold'],
                'last_updated': data['last_updated']
            }
        return data
    
    def get_coins_only(self):
        """فقط سکه‌ها را برگردان"""
        data = self.extract_all_data()
        if data['status'] == 'success':
            return {
                'status': 'success',
                'count': data['summary']['total_coins'],
                'coins': data['data']['coins'],
                'last_updated': data['last_updated']
            }
        return data
    
    def search_item(self, search_term):
        """جستجوی آیتم خاص"""
        data = self.extract_all_data()
        if data['status'] != 'success':
            return data
        
        results = []
        search_lower = search_term.lower()
        
        for category_name, category_data in data['data'].items():
            for key, item_data in category_data.items():
                if search_lower in item_data['name'].lower():
                    results.append({
                        'category': category_name,
                        'item': item_data
                    })
        
        return {
            'status': 'success',
            'search_term': search_term,
            'results_count': len(results),
            'results': results
        }
    
    def export_to_json(self, filename="tgju_data.json"):
        """صادرات به فایل JSON"""
        try:
            data = self.extract_all_data()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {'status': 'success', 'filename': filename}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
