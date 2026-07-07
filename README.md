# Django Blog

A full-stack blog application built with Django that provides a clean reading experience for visitors and a secure administration dashboard for managing blog content. The project demonstrates backend development concepts including authentication, database management, media handling, and deployment-ready configuration.

---

## Features

- User registration and authentication
- Secure administrator dashboard
- Create, edit, update, and delete blog posts
- Image upload and media management
- Responsive user interface
- Static and media file handling
- Deployment-ready configuration using WhiteNoise and Gunicorn
- Organized project structure following Django best practices

---

## Built With

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- WhiteNoise
- Gunicorn

---

## Installation

### Clone the repository

```bash
git clone https://github.com/t-shine-dev/YOUR-REPOSITORY-NAME.git
```

### Navigate to the project

```bash
cd YOUR-REPOSITORY-NAME
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

### Apply migrations

```bash
python manage.py migrate
```

### Create an administrator account (Optional)

```bash
python manage.py createsuperuser
```

### Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Project Structure

```
blog_project/
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

- **GitHub:** https://github.com/t-shine-dev
- **LinkedIn:** https://www.linkedin.com/in/temitopeolawuyi-dev
- **Portfolio:** https://t-shine-dev.github.io/backend-portfolio/

---

## License

This project is licensed under the MIT License.