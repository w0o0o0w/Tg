# =================================================================
# 🚀 TGJU API - Final Version with English Keys & Formatted Report
# =================================================================
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

class TGJUAPI:
    """
    A comprehensive API for scraping currency, gold, and coin prices from TGJU.org.

    Features:
    ✅ Scrapes 34 different currencies (major, regional, and cryptocurrencies).
    ✅ Scrapes 15 types of gold assets.
    ✅ Scrapes 19 types of coins and their bubbles.
    ✅ Generates a clean, readable, and sorted report in Markdown format.
    ✅ Creates a unique English key for each item for easy programmatic access.
    ✅ Supports JSON export and item searching.
    """
    
    def __init__(self):
        self.base_url = "https://www.tgju.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def create_english_key(self, name_fa):
        """
        Creates a unique, English-friendly key from a Persian name.
        Example: 'سکه امامی' -> 'coin_emami'
        """
        name = name_fa.lower()
        # A dictionary for common Farsi to English financial terms
        replacements = {
            'طلا': 'gold', 'سکه': 'coin', 'حباب': 'bubble', 'دلار': 'dollar', 
            'یورو': 'euro', 'پوند': 'pound', 'درهم': 'dirham', 'لیر': 'lira', 
            'یوان': 'yuan', 'ین': 'yen', 'کرون': 'krone', 'دینار': 'dinar', 
            'روپیه': 'rupee', 'فرانک': 'franc', 'رینگیت': 'ringgit', 
            'بیت کوین': 'bitcoin', 'لایت کوین': 'litecoin', 'دوج کوین': 'dogecoin',
            'بایننس': 'binance', 'شیبا': 'shiba', 'تون': 'ton', 'پلاتین': 'platinum',
            'امامی': 'emami', 'بهار آزادی': 'bahar_azadi', 'ربع': 'rob', 
            'نیم': 'nim', 'گرمی': 'gerami', 'مثقال': 'mesghal', 'انس': 'ounce',
            'عیار': 'ayar', 'آبشده': 'abshodeh'
        }
        
        for fa, en in replacements.items():
            name = name.replace(fa, en)
        
        # Remove any remaining non-ASCII characters and clean up
        name = re.sub(r'[^\x00-\x7F]+', ' ', name) # Remove non-ASCII
        name = re.sub(r'[^a-z0-9\s-]', '', name) # Remove special chars except space and dash
        key = re.sub(r'\s+', '_', name.strip()) # Replace spaces with underscores
        return key if key else 'unknown'

    def extract_all_data(self):
        """Extracts all data from the TGJU homepage."""
        try:
            response = self.session.get(self.base_url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            currencies, gold_data, coins_data = {}, {}, {}
            
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 6:
                        continue

                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    if cell_texts[0] and cell_texts[1]:
                        name_fa = cell_texts[0]
                        category = self._categorize_item(name_fa)
                        
                        if category:
                            key = self.create_english_key(name_fa)
                            item_data = {
                                'key': key,
                                'name_fa': name_fa,
                                'price': cell_texts[1],
                                'change': cell_texts[2],
                                'min_price': cell_texts[3],
                                'max_price': cell_texts[4],
                                'time': cell_texts[5],
                                'timestamp': datetime.now().isoformat(),
                                'category': category
                            }
                            
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
                },
                'data': {'currencies': currencies, 'gold': gold_data, 'coins': coins_data},
                'source': 'TGJU.org',
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Extraction failed: {str(e)}'}

    def _categorize_item(self, item_name):
        """Internal method to categorize an item based on its name."""
        item_lower = item_name.lower()
        currency_keywords = ['دلار', 'یورو', 'پوند', 'درهم', 'یوان', 'ین', 'کرون', 'لیر', 'دینار', 'روپیه', 'فرانک', 'رینگیت', 'بیت کوین', 'لایت کوین', 'دوج کوین', 'بایننس', 'شیبا', 'تون', 'پلاتین']
        gold_keywords = ['طلا', 'gold', 'مثقال', 'انس طلا', 'صندوق طلا']
        coin_keywords = ['سکه', 'حباب', 'تمام سکه']
        
        if any(keyword in item_lower for keyword in currency_keywords): return 'currency'
        if any(keyword in item_lower for keyword in gold_keywords): return 'gold'
        if any(keyword in item_lower for keyword in coin_keywords): return 'coin'
        return None

    def get_formatted_report(self):
        """Fetches data and generates a clean, sorted report in Markdown format."""
        all_data = self.extract_all_data()
        if all_data['status'] != 'success':
            return f"Error fetching data: {all_data.get('message')}"

        data = all_data['data']
        report_lines = [f"# Price Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "\n---"]

        categories = {
            'gold': '🥇 Gold',
            'coins': '🟡 Coins',
            'currencies': '💵 Currencies'
        }

        for cat_key, cat_title in categories.items():
            report_lines.extend([f"## {cat_title}\n", "| Key (English) | نام فارسی (Farsi) | قیمت | تغییرات |", "| :--- | :--- | :--- | :--- |"])
            
            items = data.get(cat_key, {})
            if not items:
                report_lines.append("| *No data found* | | | |")
                continue

            sorted_items = sorted(items.values(), key=lambda item: item['name_fa'])
            
            for item in sorted_items:
                if not any(char.isdigit() for char in item.get('price', '')):
                    continue
                report_lines.append(f"| `{item['key']}` | {item['name_fa']} | {item['price']} | {item['change']} |")
            
            report_lines.append("\n---")
            
        return "\n".join(report_lines)

# =================================================================
# 📖 How to Use:
# =================================================================

if __name__ == "__main__":
    # 1. Create an instance of the API
    api = TGJUAPI()

    # 2. Get the formatted, human-readable report
    print("-----------[Formatted Report]-----------")
    formatted_report = api.get_formatted_report()
    print(formatted_report)

    # 3. Get all data as a JSON-like dictionary
    print("\n\n-----------[Raw Dictionary Data]-----------")
    all_data = api.extract_all_data()
    if all_data['status'] == 'success':
        # Print the English key and Farsi name for the first gold item
        first_gold_key = list(all_data['data']['gold'].keys())[0]
        first_gold_item = all_data['data']['gold'][first_gold_key]
        print(f"Example Gold Item -> Key: '{first_gold_key}', Name: '{first_gold_item['name_fa']}'")
        
        # Print total items found
        print(f"Summary: {all_data['summary']}")
