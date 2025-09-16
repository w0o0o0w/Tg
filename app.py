# app.py
from flask import Flask, jsonify, request
from tg import TGJUCompleteAPI  # وارد کردن کلاس از فایل tg.py

# ساخت یک نمونه از اپلیکیشن فلسک
app = Flask(__name__)
# ساخت یک نمونه از کلاس API شما
api = TGJUCompleteAPI()

# این مسیر، صفحه اصلی وب‌سرویس را نمایش می‌دهد
@app.route('/')
def home():
    return "به وب‌سرویس قیمت ارز، طلا و سکه خوش آمدید! از مسیرهای /all, /currencies, /gold, /coins استفاده کنید."

# مسیر دریافت تمام داده‌ها
@app.route('/all')
def get_all_data():
    data = api.extract_all_data()
    return jsonify(data)

# مسیر دریافت فقط ارزها
@app.route('/currencies')
def get_currencies():
    data = api.get_currencies_only()
    return jsonify(data)

# مسیر دریافت فقط طلا
@app.route('/gold')
def get_gold():
    data = api.get_gold_only()
    return jsonify(data)

# مسیر دریافت فقط سکه‌ها
@app.route('/coins')
def get_coins():
    data = api.get_coins_only()
    return jsonify(data)

# مسیر جستجو
# مثال: /search?q=دلار
@app.route('/search')
def search():
    # دریافت عبارت جستجو از URL
    query = request.args.get('q')
    if not query:
        return jsonify({'status': 'error', 'message': 'لطفا یک عبارت برای جستجو در پارامتر q وارد کنید.'}), 400
    
    data = api.search_item(query)
    return jsonify(data)
