# Gitga Yuklash Yo'riqnomasi

Bu yo'riqnoma UyKelishuvBot_V1 loyihasini GitHub ga to'g'ri yuklash uchun yozilgan.

## 📋 Oldindan Tayyorlash

### 1. GitHub da Repository Yaratish

1. **GitHub.com ga kiring**
2. **"New repository" tugmasini bosing**
3. **Repository nomini kiriting**: `UyKelishuvBot_V1`
4. **Description**: "Uzbekistonda uy-joy kelishuvi uchun Telegram bot"
5. **Public yoki Private tanlang**
6. **"Create repository" tugmasini bosing**

### 2. Git O'rnatish (Agar o'rnatilmagan bo'lsa)

**Windows:**
- [Git for Windows](https://git-scm.com/download/win) dan yuklab oling
- O'rnatish jarayonida default sozlamalarni qoldiring

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt update
sudo apt install git
```

## 🚀 Gitga Yuklash Jarayoni

### 1. Terminal/Command Prompt Ochish

**Windows:**
- `Win + R` → `cmd` → Enter
- Yoki PowerShell oching

**Mac/Linux:**
- Terminal oching

### 2. Loyiha Papkasiga O'tish

```bash
cd F:\UyKelishuvBot\UyKelishuvBot_V1
```

### 3. Git Repository Boshlash

```bash
git init
```

### 4. Barcha Fayllarni Qo'shish

```bash
git add .
```

### 5. Birinchi Commit Yaratish

```bash
git commit -m "Initial commit - UyKelishuv Bot V1"
```

### 6. GitHub Repository ni Ulash

```bash
git remote add origin https://github.com/YOUR_USERNAME/UyKelishuvBot_V1.git
```

**Eslatma:** `YOUR_USERNAME` o'rniga o'zingizning GitHub usernameingizni yozing.

### 7. Asosiy Branch ni Nomlash

```bash
git branch -M main
```

### 8. GitHub ga Yuklash

```bash
git push -u origin main
```

## 🔐 GitHub Authentication

### SSH Key (Tavsiya etiladi)

**1. SSH Key Yaratish:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**2. SSH Key ni GitHub ga Qo'shish:**
1. GitHub → Settings → SSH and GPG keys
2. "New SSH key" tugmasini bosing
3. Key ni nusxalang va qo'shing

**3. SSH orqali Clone:**
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/UyKelishuvBot_V1.git
```

### Personal Access Token

**1. Token Yaratish:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" tugmasini bosing
3. "repo" scope ni tanlang
4. Token ni nusxalang

**2. Token orqali Push:**
```bash
git push -u origin main
# Username: YOUR_USERNAME
# Password: YOUR_TOKEN
```

## 📁 Yuklanadigan Fayllar

### ✅ Yuklanadigan Fayllar
```
UyKelishuvBot_V1/
├── src/                    # Source kodlar
│   ├── bot/               # Bot logikasi
│   ├── database/          # Database modellari
│   ├── services/          # Biznes logikasi
│   └── utils/             # Yordamchi funksiyalar
├── alembic/               # Database migrationlar
├── alembic.ini           # Alembic konfiguratsiyasi
├── requirements.txt       # Python dependencies
├── start_bot.py          # Bot ishga tushirish
├── env.example           # Environment variables namunasi
├── README.md             # Loyiha dokumentatsiyasi
└── .gitignore            # Git ignore qoidalari
```

### ❌ Yuklanmaydigan Fayllar
```
❌ .env                   # Shaxsiy konfiguratsiya
❌ *.db                   # Database fayllar
❌ __pycache__/          # Python cache
❌ venv/                 # Virtual environment
❌ *.log                 # Log fayllar
❌ .vscode/              # IDE sozlamalari
❌ .idea/                # IDE sozlamalari
```

## 🔄 Keyingi O'zgarishlar

### Yangi O'zgarishlar Qo'shish

```bash
# O'zgarishlarni ko'rish
git status

# Fayllarni qo'shish
git add .

# Commit yaratish
git commit -m "O'zgarish tavsifi"

# GitHub ga yuklash
git push
```

### Branch Yaratish

```bash
# Yangi branch yaratish
git checkout -b feature/yangi-xususiyat

# O'zgarishlar qilish va commit
git add .
git commit -m "Yangi xususiyat qo'shildi"

# Branch ni push qilish
git push -u origin feature/yangi-xususiyat
```

## 🚨 Xatoliklar va Yechimlar

### "Repository already exists" Xatoligi

```bash
# Remote ni o'chirish
git remote remove origin

# Qayta qo'shish
git remote add origin https://github.com/YOUR_USERNAME/UyKelishuvBot_V1.git
```

### "Authentication failed" Xatoligi

```bash
# Credential ni tozalash
git config --global --unset user.name
git config --global --unset user.email

# Qayta sozlash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

### "Large file" Xatoligi

```bash
# .gitignore ga qo'shish
echo "*.db" >> .gitignore
echo "*.log" >> .gitignore

# Cache ni tozalash
git rm --cached *.db
git rm --cached *.log

# Qayta commit
git add .gitignore
git commit -m "Update .gitignore"
git push
```

## 📋 Tekshirish Ro'yxati

Yuklashdan oldin tekshiring:

- [ ] `.env` fayli yo'q
- [ ] `*.db` fayllar yo'q
- [ ] `__pycache__/` papkalar yo'q
- [ ] `venv/` papka yo'q
- [ ] `.gitignore` fayli mavjud
- [ ] `README.md` fayli mavjud
- [ ] `requirements.txt` fayli mavjud
- [ ] Barcha source kodlar mavjud

## 🎯 Muvaffaqiyatli Yuklashdan Keyin

1. **GitHub da repository ni tekshiring**
2. **README.md to'g'ri ko'rinishini tekshiring**
3. **Barcha fayllar mavjudligini tekshiring**
4. **Railway.com da deploy qilishga tayyorlaning**

## 📞 Yordam

Agar muammo bo'lsa:
1. Xatolik xabarini nusxalang
2. `git status` natijasini ko'ring
3. `git log --oneline` bilan commitlar ro'yxatini ko'ring
4. GitHub Issues da muammoni bildiring

---

**Muvaffaqiyatli yuklash!** 🚀
