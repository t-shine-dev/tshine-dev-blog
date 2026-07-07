# Django Blog

A full-stack blog application built with Django that provides a clean reading experience for visitors and a secure administration dashboard for managing blog content.

The project demonstrates backend development concepts including authentication, database management, media handling, static file configuration, and production deployment.

---

## Live Demo

🌐 **Website:** https://temitopeolawuyi.pythonanywhere.com/

---

## Features

* User registration and authentication
* Secure administrator dashboard
* Create, read, update, and delete blog posts (CRUD)
* Image upload and media management
* Responsive user interface
* Static and media file handling
* Production-ready configuration using WhiteNoise
* Organized project structure following Django best practices

---

## Built With

* Python
* Django
* HTML5
* CSS3
* JavaScript
* SQLite
* WhiteNoise
* Gunicorn

---

## Installation

### Clone the repository

```bash
git clone https://github.com/t-shine-dev/tshine-dev-blog.git
```

### Navigate to the project

```bash
cd tshine-dev-blog
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create environment variables

Create a `.env` file and add:

```env
BLOG_SECRET_KEY=your-secret-key
BLOG_DEBUG=True
```

### Apply migrations

```bash
python manage.py migrate
```

### Create an administrator account

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

## Deployment

The project is deployed using:

* PythonAnywhere
* WhiteNoise for static files
* Production Django settings
* Git-based deployment workflow

---

## Project Structure

```
tshine-dev-blog/
│
├── blog/
├── blog_project/
├── media/
├── staticfiles/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Author

**Temitope Olawuyi**

Frontend & Backend Developer

* GitHub: https://github.com/t-shine-dev
* LinkedIn: https://www.linkedin.com/in/temitopeolawuyi-dev
* Portfolio: https://t-shine4.github.io/portfolio/

---

## License

This project is licensed under the MIT License.
