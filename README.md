# 🌹 ورود الحب - Worood Al-Hub

<div align="center">

![ورود الحب](https://img.shields.io/badge/ورود%20الحب-v1.0-e8547a?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**برنامج متكامل لعرض خلفيات وصور الورود والطبيعة**

*A complete desktop application for displaying roses and nature wallpapers*

</div>

---

## ✨ المميزات

| الميزة | الوصف |
|--------|-------|
| 🖼 **معرض صور متكامل** | عرض جميع الصور في واجهة أنيقة |
| 📂 **تصنيف الصور** | تصفية حسب الفئة (ورود حمراء، وردية، بيضاء، صفراء، طبيعة) |
| ▶ **عرض تلقائي** | شرائح تلقائية مع التحكم في السرعة |
| ❤ **المفضلة** | حفظ الصور المفضلة والوصول إليها بسهولة |
| 🔍 **تكبير وتصغير** | التحكم في حجم الصورة بالماوس أو الأزرار |
| 🎨 **تأثيرات الصور** | تأثير ضبابي، تحسين الألوان، تدوير، قلب |
| ⛶ **ملء الشاشة** | وضع ملء الشاشة للاستمتاع بالصور |
| 💾 **حفظ الصور** | حفظ الصور المعدلة بصيغ مختلفة |
| 🖨 **خلفية سطح المكتب** | تعيين أي صورة كخلفية سطح المكتب |
| 🎲 **صورة عشوائية** | اختيار صورة عشوائية بضغطة زر |
| 💬 **اقتباسات رومانسية** | اقتباسات متحركة عن الحب والورود |

---

## 📸 الصور المضمنة

يحتوي البرنامج على **24 صورة** مقسمة إلى فئات:

- 🔴 **ورود حمراء** - 3 صور
- 🌸 **ورود وردية** - 5 صور
- ⚪ **ورود بيضاء** - 3 صور
- 🟡 **ورود صفراء** - 3 صور
- ❤ **ورود الحب** - 2 صور
- 🌿 **طبيعة وزهور** - 8 صور

---

## 🚀 التثبيت والتشغيل

### المتطلبات

```bash
Python 3.8 أو أحدث
tkinter (مضمن مع Python)
Pillow
```

### خطوات التثبيت

```bash
# 1. استنساخ المستودع
git clone https://github.com/adnan0094/worood-alhub.git
cd worood-alhub

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تشغيل البرنامج
python main.py
```

### على Linux (Ubuntu/Debian)

```bash
# تثبيت tkinter
sudo apt-get install python3-tk

# تثبيت Pillow
pip install Pillow

# تشغيل البرنامج
python3 main.py
```

---

## ⌨️ اختصارات لوحة المفاتيح

| المفتاح | الوظيفة |
|---------|---------|
| `←` `→` | التنقل بين الصور |
| `Space` | تشغيل/إيقاف العرض التلقائي |
| `F11` | ملء الشاشة |
| `Escape` | الخروج من ملء الشاشة |
| `F` | إضافة/إزالة من المفضلة |
| `+` | تكبير |
| `-` | تصغير |
| `0` | إعادة الحجم الأصلي |

---

## 🗂 هيكل المشروع

```
worood-alhub/
│
├── main.py              # الملف الرئيسي للبرنامج
├── requirements.txt     # متطلبات Python
├── README.md            # توثيق المشروع
├── settings.json        # إعدادات البرنامج (يُنشأ تلقائياً)
│
└── images/              # مجلد الصور
    ├── rose_red_01.jpg
    ├── rose_red_02.jpg
    ├── rose_pink_01.jpg
    ├── rose_pink_tunnel.jpg
    ├── rose_white_01.jpg
    ├── rose_yellow_01.jpg
    ├── rose_love_heart.jpg
    ├── nature_flowers_01.jpg
    └── ... (24 صورة إجمالاً)
```

---

## 🎨 لقطات الشاشة

> البرنامج يعمل على نظام Linux مع واجهة مستخدم رسومية أنيقة بألوان داكنة وردية.

---

## 🛠 التقنيات المستخدمة

- **Python 3** - لغة البرمجة الرئيسية
- **Tkinter** - مكتبة الواجهة الرسومية
- **Pillow (PIL)** - معالجة وعرض الصور
- **Threading** - للعرض التلقائي والتحميل في الخلفية
- **JSON** - حفظ الإعدادات والمفضلة

---

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 المطور

**Adnan** - [@adnan0094](https://github.com/adnan0094)

---

<div align="center">

صُنع بـ ❤ وورود 🌹

*Made with love and roses*

</div>
