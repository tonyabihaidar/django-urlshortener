# 🚀 URL Shortener & QR Generator
### A Modern, Cloud-Deployed, Full-Stack Django Web App

Welcome to **QURL**, a fully featured, production-ready web application built with **Django**, designed to shorten long URLs, generate QR codes, create custom vanity links, and offer private analytics for logged-in users — all deployed seamlessly on **Microsoft Azure App Service** with CI/CD.

---

## 🌐 Live Demo on Azure

Try it here:  
👉 **https://urlshortener-dresf9dzctahange.francecentral-01.azurewebsites.net/link/WJ1j5v/**  

---

# 📌 Features

### 🔗 URL Shortening
- Convert long URLs into short, clean, shareable links.
- Optionally add a **custom slug** (vanity code).
- Automatic conflict checking.

### 👤 User Accounts & Dashboards
- Secure sign up / login/logout.
- Each user has **private access** to their own saved links.
- See creation dates & (optional) analytics.

### 📷 QR Code Generation
- Every shortened URL has an automatically generated QR code.
- Users can:
  - Download QR code as PNG  
  - Share QR code through mobile share API  
  - Reuse the QR anywhere (flyers, posters, websites)

### 🎨 Modern UI
Built with **Bulma CSS** for clean, mobile-friendly pages:
- Signup & login pages
- Link-creation form
- “My Links” dashboard
- Stylish link details page with copy/share/download buttons

### ☁️ Cloud Deployment on Azure
- Azure App Service (Linux)
- GitHub Actions CI/CD pipeline
- Environment-variable-based secrets
- Static file handling in production
- CSRF & allowed hosts fully configured

---

# 🛠️ Tech Stack

**Backend:**  
- Django 5  
- Django ORM  
- Built-in authentication  
- Custom slug + redirect logic  
- QR code generation (Python `qrcode`)

**Frontend:**  
- Bulma CSS  
- JavaScript for copy/share buttons  
- Responsive templates  

**DevOps & Cloud:**  
- Microsoft Azure App Service  
- GitHub Actions Deployment  
- Environment variables for production  
- Debug-secure setup  

---

# 📸 Screenshots

> Add your screenshots in a `/screenshots` folder and link them here:
- `screenshots/login.png`
- `screenshots/signup.png`
- `screenshots/home.png`
- `screenshots/my_links.png`
- `screenshots/details.png`

---

# 🧪 Local Setup Guide

### 1️⃣ Clone the project
```bash
git clone https://github.com/yourusername/django-urlshortener.git
cd django-urlshortener
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
```

Activate it:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment
Create a `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
```

### 5️⃣ Migrate
```bash
python manage.py migrate
```

### 6️⃣ Run locally
```bash
python manage.py runserver
```

---

# ☁️ Azure Deployment Guide (Simplified)

1. Create Azure App Service (Linux, Python 3.10).  
2. Add these environment variables under **Configuration → Application Settings**:

```
SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_ALLOWED_HOSTS=urlshortener-xxxx.azurewebsites.net
DJANGO_CSRF_TRUSTED_ORIGINS=https://urlshortener-xxxx.azurewebsites.net
```

3. Push code to GitHub — this triggers GitHub Actions CI/CD.  
4. Azure deploys automatically.  
5. Visit your live site:  
   `https://urlshortener-xxxx.azurewebsites.net/`

---
