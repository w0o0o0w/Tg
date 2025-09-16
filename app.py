# app.py
from flask import Flask, jsonify, request
from tg import TGJUCompleteAPI

app = Flask(__name__)
# =====> این خط جدید را اضافه کنید <=====
app.json.ensure_ascii = False 
# =======================================
api = TGJUCompleteAPI()

@app.route('/')
def home():
    return "به وب‌سرویس قیمت ارز، طلا و سکه خوش آمدید! از مسیرهای /all, /currencies, /gold, /coins استفاده کنید."

# ... (بقیه کدهای شما بدون تغییر باقی می‌مانند) ...

@app.route('/all')
def get_all_data():
    data = api.extract_all_data()
    return jsonify(data)

@app.route('/currencies')
def get_currencies():
    data = api.get_currencies_only()
    return jsonify(data)

@app.route('/gold')
def get_gold():
    data = api.get_gold_only()
    return jsonify(data)

@app.route('/coins')
def get_coins():
    data = api.get_coins_only()
    return jsonify(data)

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'status': 'error', 'message': 'لطفا یک عبارت برای جستجو در پارامتر q وارد کنید.'}), 400
    
    data = api.search_item(query)
    return jsonify(data)
