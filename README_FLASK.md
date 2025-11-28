# AUTO REZYUME - Flask Application

Sayt nomi: **AUTO REZYUME**  
Sayt nuri: Foydalanuvchiga rezyume yaratish, tahrirlash va yuklab olish imkoniyati.

## 🔧 Texnologiyalar

- **Backend:** Python (Flask)
- **Frontend:** HTML + CSS + Bootstrap 5
- **Database:** MySQL
- **Password Security:** Werkzeug

## 📁 Fayl Tuzilmasi

```
auto_rezyume/
├── app.py                    # Asosiy Flask application
├── database.py              # MySQL ulanish
├── schema.sql               # Database schema
├── requirements_flask.txt   # Python dependencies
├── templates/               # HTML templates
│   ├── index.html          # Bosh sahifa
│   ├── register.html       # Ro'yxatdan o'tish
│   ├── login.html          # Kirish
│   ├── dashboard.html      # Boshqarish paneli
│   ├── resume_form.html    # Rezyume yaratish
│   └── resume_view.html    # Rezyume ko'rish
└── static/                 # Statik fayllar
    ├── css/                # CSS fayllar
    ├── js/                 # JavaScript fayllar
    └── img/                # Rasmlar
```

## 🚀 Ishga Tushirish

### 1. MySQL Bazasini Yaratish

```bash
mysql -u root -p < schema.sql
```

Yoki MySQL client orqali:
```sql
CREATE DATABASE IF NOT EXISTS auto_rezyume CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 2. Python Dependency'larini O'rnatish

```bash
pip install -r requirements_flask.txt
```

### 3. Database Credentials'ni Yangilash

`database.py` faylida MySQL parolingizni o'rnating:
```python
password=''  # o'zingizning MySQL parolingiz
```

### 4. Flask Applicationni Ishga Tushirish

```bash
python app.py
```

Server http://127.0.0.1:5000 da ishga tushadi.

## 📄 Sahifalar va Funksiyalar

| Sahifa | URL | Maqsad |
|--------|-----|--------|
| Bosh sahifa | `/` | Sayt haqida ma'lumot + "Boshlash" tugmasi |
| Ro'yxatdan o'tish | `/register` | Yangi foydalanuvchi yaratish |
| Kirish | `/login` | Mavjud foydalanuvchi kirishi |
| Dashboard | `/dashboard` | Foydalanuvchining rezyumelari ro'yxati |
| Yangi Rezyume | `/create_resume` | Rezyume yaratish formasi |
| Rezyume Ko'rish | `/resume/<id>` | Rezyume shakloni ko'rish |
| Chiqish | `/logout` | Sessiyani tugatish |

## 🔐 Xavfsizlik

- Parollar `Werkzeug.security` orqali bcrypt bilan hashlangan.
- Sessiya management Flask bilan amalga oshiriladi.
- SQL injection qo'lga olingan (parameterized queries).

## 🎨 Dizayn

- Bootstrap 5 framework
- Gradient background
- Responsive design (barcha qurilmalar)
- Modern glassmorphism effekti

## 💡 Kerakli Qo'shimchalar (Keyingi bosqichlar)

- PDF generatsiya (WeasyPrint)
- Fayl yuklash (profil rasmi, CV)
- Email verification
- Rezyume shablonlari
- Izoh va reyting tizimi
