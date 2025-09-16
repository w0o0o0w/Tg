# app.py
from flask import Flask, jsonify, request
from tg import TGJUAPI  # <--- تصحیح شد: نام کلاس به TGJUAPI تغییر کرد
from datetime import datetime, timedelta
import time

# --- راه‌اندازی اپلیکیشن فلسک ---
app = Flask(__name__)
app.json.ensure_ascii = False  # برای نمایش صحیح کاراکترهای فارسی در خروجی
api = TGJUAPI()  # <--- تصحیح شد: از نام کلاس جدید استفاده شد

# =======================================================
# بخش مربوط به کش کردن اطلاعات (Caching)
# =======================================================
cached_data = None
last_fetch_time = None
CACHE_DURATION_MINUTES = 5
# =======================================================


# --- تعریف مسیرهای API ---

@app.route('/')
def home():
    """صفحه اصلی برای نمایش پیام خوش‌آمدگویی."""
    return " به وب‌سرویس قیمت ارز، طلا و سکه خوش آمدید ÐΛɌ₭ᑎΞ𐒡𐒡🗽𓄂𓆃 Tel=@mansor427!"

@app.route('/all')
def get_all_data():
    """
    تمام اطلاعات را برمی‌گرداند.
    این مسیر از سیستم کش ۵ دقیقه‌ای استفاده می‌کند.
    """
    global cached_data, last_fetch_time

    # بررسی می‌کنیم که آیا داده‌ای در کش وجود دارد و هنوز معتبر است یا نه
    if cached_data and last_fetch_time and (datetime.now() - last_fetch_time) < timedelta(minutes=CACHE_DURATION_MINUTES):
        print("ارسال اطلاعات از کش (CACHE)...")
        return jsonify(cached_data)
    
    # --- منطق زمان‌سنجی ---
    start_time = time.time()
    print("در حال دریافت اطلاعات جدید از TGJU.org...")
    
    new_data = api.extract_all_data()
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"===> زمان استخراج اطلاعات: {duration:.2f} ثانیه.")
    # --- پایان زمان‌سنجی ---
    
    # اگر دریافت اطلاعات موفق بود، آن را در کش ذخیره می‌کنیم
    if new_data and new_data.get('status') == 'success':
        cached_data = new_data
        last_fetch_time = datetime.now()
        
    return jsonify(new_data)


@app.route('/currencies')
def get_currencies():
    """فقط اطلاعات ارزها را به صورت زنده برمی‌گرداند."""
    data = api.get_currencies_only()
    return jsonify(data)


@app.route('/gold')
def get_gold():
    """فقط اطلاعات طلا را به صورت زنده برمی‌گرداند."""
    data = api.get_gold_only()
    return jsonify(data)


@app.route('/coins')
def get_coins():
    """فقط اطلاعات سکه‌ها را به صورت زنده برمی‌گرداند."""
    data = api.get_coins_only()
    return jsonify(data)


@app.route('/search')
def search():
    """یک آیتم خاص را جستجو می‌کند."""
    query = request.args.get('q')
    if not query:
        return jsonify({'status': 'error', 'message': 'لطفا یک عبارت برای جستجو در پارامتر q وارد کنید.'}), 400
    
    data = api.search_item(query)
    return jsonify(data)
