# TShine Dev Blog 🌟

A full-stack blog application built with Django that provides a clean, modern reading experience for developers and a secure administration dashboard for managing blog content.

The project demonstrates backend development concepts including user authentication, database management, media upload handling, custom CSS styling, static file optimization, and production deployment.

---

## 🚀 Live Demo

🌐 Website: https://temitopeolawuyi.pythonanywhere.com/

---

## 📸 Preview

### Homepage

![Homepage Screenshot](screenshots/homepage.png)

### Creator Dashboard

![Dashboard Screenshot](screenshots/dashboard.png)

---

## ✨ Features

### 🔐 User Authentication & Security

* User registration and login system
* Secure session-based authentication
* Protected dashboard access

### 📝 Blog Management (CRUD)

* Create blog posts
* Read published articles
* Update existing posts
* Delete posts

### 🖼️ Media Management

* Image uploads for blog articles
* Media file handling and storage

### 📱 Responsive Design

* Clean user interface
* Responsive layout across different screen sizes
* Custom CSS styling

### ⚙️ Production Configuration

* Static file management using WhiteNoise
* Optimized static file serving
* Production-ready Django configuration
* Deployment on PythonAnywhere

---

## 🖥️ Creator Dashboard

The administration dashboard provides content creators with a dedicated space to manage blog posts and maintain website content efficiently.

---

## 🛠️ Built With

### Backend

* Python
* Django 6.0+

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite (Development)

### Production Tools

* WhiteNoise
* PythonAnywhere Deployment

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/t-shine-dev/tshine-dev-blog.git
```

## 2. Navigate into the project directory

```bash
cd tshine-dev-blog
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configure environment variables

Create a `.env` file in the project root:

```env
BLOG_SECRET_KEY=your-secret-key
BLOG_DEBUG=True
```

For production:

```env
BLOG_DEBUG=False
```

## 7. Apply database migrations

```bash
python manage.py migrate
```

## 8. Create an administrator account

```bash
python manage.py createsuperuser
```

## 9. Run the development server

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

# 🌍 Deployment

The application is deployed on PythonAnywhere with:

* Production Django settings
* WhiteNoise for optimized static file serving
* Secure `DEBUG=False` configuration
* Git-based deployment workflow

---

# 📂 Project Structure

```
tshine-dev-blog/
│
├── blog/                    # Blog application (models, views, templates, URLs)
├── blog_project/            # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/                   # Uploaded images and media files
├── staticfiles/             # Collected production static files
├── manage.py                # Django management script
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

---

# 👤 Author

**Temitope Olawuyi**

Frontend & Backend Developer

* GitHub: https://github.com/t-shine-dev
* LinkedIn: https://www.linkedin.com/in/temitopeolawuyi-dev
* Portfolio: https://t-shine4.github.io/portfolio/

---

# 📄 License

This project is licensed under the MIT License.
