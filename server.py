"""سرور داده. اجرا:  python3 server.py   (پیش‌فرض: حالت DEMO)
حالت واقعی:  DEMO=0 python3 server.py  و تکمیل تابع fetch_real()
خروجی /api/market: لیستی از
 {n: نماد, base: قیمت پایانی دیروز, hb: قدرت خریدار حقیقی, lb: قدرت خریدار حقوقی,
  c:[...], h:[...], l:[...]}   حداقل ۱۲۰ کندل روزانه؛ آخرین کندل = قیمت لحظه‌ای"""
import json, os, random, time
from http.server import BaseHTTPRequestHandler, HTTPServer

def fetch_demo():
    names = "فولاد شپنا خودرو وبملت فملی شستا کگل وتجارت خساپا اخابر شبندر پترول فارس حفارس کچاد ومعادن وبصادر تاپیکو دی شتران خگستر فپنتا کروی ذوب".split()
    out = []
    for n in names:
        r = random.Random(n); p = 1500 + r.random() * 9000; c = []; h = []; l = []
        dr = (r.random() - .5) * .012
        for k in range(120):
            p *= 1 + dr * (-1 if k > 80 else 1) + (r.random() - .5) * .045
            c.append(p); h.append(p * (1 + r.random() * .015)); l.append(p * (1 - r.random() * .015))
        c[-1] *= 1 + (random.random() - .5) * .004
        out.append(dict(n=n, base=c[-2], hb=.5 + r.random() * 3, lb=.2 + r.random() * 2.5, c=c, h=h, l=l))
    return out

def fetch_real():
    # TODO: اتصال به TSETMC. کتابخانه‌های پیشنهادی (روی سرور، نه داخل اپ):
    #   pip install tsetmc        (https://github.com/5j9/tsetmc)  -> MarketWatch و تاریخچه
    #   npm i tse-client          (https://github.com/omiom33/tse-client2) -> کندل‌های روزانه
    # برای هر نماد، ۱۲۰ کندل آخر + قیمت لحظه‌ای را به قالب بالا درآورید.
    # قدرت خریدار = (ارزش خرید ÷ تعداد خریدار) ÷ (ارزش فروش ÷ تعداد فروشنده)، جدا برای حقیقی و حقوقی.
    # کدال (codal.ir) برای اطلاعیه‌هاست و آدرس‌های آن رسمی/پایدار نیست؛ بعداً جدا اضافه می‌شود.
    raise NotImplementedError

cache = {"t": 0, "d": []}
def data():
    if time.time() - cache["t"] > 5:      # حداکثر هر ۵ ثانیه یک بار به منبع می‌رویم
        cache["d"] = fetch_demo() if os.environ.get("DEMO", "1") == "1" else fetch_real()
        cache["t"] = time.time()
    return cache["d"]

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/api/market":
            self.send_response(404); self.end_headers(); return
        try: body = json.dumps(data(), ensure_ascii=False).encode()
        except Exception as e:
            self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode()); return
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers(); self.wfile.write(body)

HTTPServer(("0.0.0.0", 8000), H).serve_forever()
