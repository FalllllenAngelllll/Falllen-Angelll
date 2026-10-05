# ساخت APK دیده‌بان بورس

نیازها: Node.js 18+، Android Studio، Python 3

1. سرور (روی کامپیوتر یا VPS):
   cd server && python3 server.py
   (آدرس IP سرور را در www/index.html، متغیر API، بگذارید)
2. ساخت اپ:
   npm install
   npx cap add android
   npx cap sync android
   npx cap open android
3. در Android Studio: Build > Build APK(s)  (برای انتشار: Generate Signed Bundle/APK)

بعد از هر تغییر در www/index.html دوباره: npx cap sync android
