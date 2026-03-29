@echo off
title 🌹 ورود الحب - تشغيل تلقائي 🌹
color 0D
echo.
echo  ==========================================================
echo            🌹 مرحبا بك في برنامج ورود الحب 🌹
echo  ==========================================================
echo.
echo  [+] جاري التحقق من المتطلبات وتشغيل البرنامج...
echo.

:: التحقق من وجود بايثون
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] بايثون غير مثبت على جهازك!
    echo  [!] يرجى تحميل وتثبيت بايثون من: https://www.python.org/downloads/
    echo  [!] تأكد من تفعيل خيار "Add Python to PATH" أثناء التثبيت.
    pause
    exit
)

:: تثبيت المكتبات المطلوبة
echo  [+] جاري تثبيت المكتبات اللازمة (Pillow, OpenCV, Requests)...
pip install -r requirements.txt --quiet

:: تشغيل البرنامج
echo.
echo  [+] تم بنجاح! جاري تشغيل ورود الحب الآن... 🌹
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo  [!] حدث خطأ أثناء تشغيل البرنامج.
    pause
)
