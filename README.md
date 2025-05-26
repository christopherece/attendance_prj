<div align="center">

# ✨ VisitorPass ✨

[![Django](https://img.shields.io/badge/Django-4.2.5-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*A modern digital visitor management system built with Django*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Deployment](#deployment)

</div>

## 📋 Overview

VisitorPass is a comprehensive visitor management solution designed to streamline the check-in process for organizations of all sizes. The system allows visitors to sign in digitally, automatically notifies staff of visitor arrivals via email, and provides robust reporting and analytics capabilities.

## ✨ Features

<table>
  <tr>
    <td>
      <h3>🔐 Visitor Management</h3>
      <ul>
        <li>Simple and intuitive sign-in interface</li>
        <li>Automatic staff notifications via email</li>
        <li>Digital sign-out process</li>
        <li>Visitor tracking and history</li>
      </ul>
    </td>
    <td>
      <h3>📊 Analytics & Reporting</h3>
      <ul>
        <li>Comprehensive dashboard with visitor statistics</li>
        <li>Daily, weekly, and monthly reports</li>
        <li>Custom date range reporting</li>
        <li>Data visualization with charts and graphs</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>👥 Staff Management</h3>
      <ul>
        <li>Add and manage staff members</li>
        <li>Track most visited staff</li>
        <li>Staff email integration</li>
        <li>Staff visit history</li>
      </ul>
    </td>
    <td>
      <h3>🛠️ Administration</h3>
      <ul>
        <li>Secure admin portal</li>
        <li>User authentication and authorization</li>
        <li>Data export capabilities (CSV)</li>
        <li>System configuration options</li>
      </ul>
    </td>
  </tr>
</table>

## 🛠️ Technology Stack

<table>
  <tr>
    <td>
      <h3>Backend</h3>
      <ul>
        <li><img src="https://img.shields.io/badge/Django-4.2.5-092E20?style=flat&logo=django&logoColor=white" alt="Django"></li>
        <li><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></li>
      </ul>
    </td>
    <td>
      <h3>Frontend</h3>
      <ul>
        <li><img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white" alt="HTML5"></li>
        <li><img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white" alt="CSS3"></li>
        <li><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" alt="JavaScript"></li>
        <li><img src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=bootstrap&logoColor=white" alt="Bootstrap"></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>Database</h3>
      <ul>
        <li><img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white" alt="SQLite"></li>
        <li><img src="https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL"></li>
      </ul>
    </td>
    <td>
      <h3>Other</h3>
      <ul>
        <li><img src="https://img.shields.io/badge/SMTP-Email-005FF9?style=flat&logo=mail.ru&logoColor=white" alt="SMTP Email"></li>
        <li><img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker"></li>
      </ul>
    </td>
  </tr>
</table>

## 💻 Installation

### Prerequisites

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
<img src="https://img.shields.io/badge/pip-latest-orange?style=for-the-badge&logo=pypi&logoColor=white" alt="pip">

### 📍 Quick Start Guide

<details>
<summary>Click to expand installation steps</summary>

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/visitorpass.git
   cd visitorpass
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Visitor interface: [http://localhost:8000](http://localhost:8000)
   - Admin portal: [http://localhost:8000/admin-portal/](http://localhost:8000/admin-portal/)
   - Django admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

</details>

## 📂 Project Structure

```
visitorpass/
├── admin_portal/    # Admin interface and dashboard
├── report/          # Reporting and analytics functionality
├── static/          # Static files (CSS, JS, images)
├── templates/       # HTML templates
├── visitor/         # Core visitor management functionality
├── visitorpass/     # Project settings and configuration
├── manage.py        # Django management script
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## ⚙️ Configuration

<details>
<summary><b>Email Configuration</b></summary>

Configure email settings in `settings.py`:

```python
# Email settings
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
EMAIL_USE_TLS = True

# For development, use console backend to avoid SSL issues
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
</details>

<details>
<summary><b>Database Configuration</b></summary>

The application is configured to use SQLite by default. To use PostgreSQL, update the database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'visitor_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',  # or your database host
        'PORT': '5432',
    }
}
```
</details>

## 📝 Usage

<div align="center">
  <img src="https://topitsolutions.co.nz/media/portfolio/Screenshot_2025-05-21_at_7.45.13PM.png" alt="VisitorPass Screenshot" width="80%">
  <p><i></i></p>
</div>

### 🚸 Visitor Flow

<table>
  <tr>
    <td width="80"><b>Step 1</b></td>
    <td>Visitor arrives and uses the sign-in interface</td>
  </tr>
  <tr>
    <td><b>Step 2</b></td>
    <td>Visitor selects the staff member they're visiting</td>
  </tr>
  <tr>
    <td><b>Step 3</b></td>
    <td>System notifies the staff member via email</td>
  </tr>
  <tr>
    <td><b>Step 4</b></td>
    <td>Visitor signs out when leaving</td>
  </tr>
</table>

### 💻 Admin Portal

<table>
  <tr>
    <td width="80"><b>Step 1</b></td>
    <td>Access the admin portal at <code>/admin-portal/</code></td>
  </tr>
  <tr>
    <td><b>Step 2</b></td>
    <td>Log in with admin credentials</td>
  </tr>
  <tr>
    <td><b>Step 3</b></td>
    <td>View dashboard, manage staff, and generate reports</td>
  </tr>
</table>

## 🚀 Deployment

<div align="center">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Ready">
  <img src="https://img.shields.io/badge/WSGI-Compatible-009688?style=for-the-badge&logo=python&logoColor=white" alt="WSGI Compatible">
  <img src="https://img.shields.io/badge/Cloud-Ready-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Cloud Ready">
</div>

The application includes a Dockerfile for containerized deployment. It can be deployed to various platforms:

<details>
<summary><b>Docker Deployment</b></summary>

### Running with Docker

```bash
# Build the Docker image
docker build -t visitorpass .

# Run the container
docker run -p 8000:8000 visitorpass
```

### Running with Docker Compose

```bash
# Start the application with PostgreSQL
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Multi-Architecture Support

This application supports both ARM (Apple Silicon, Raspberry Pi) and x86 architectures. The GitHub Actions workflow automatically builds and publishes multi-architecture images to Docker Hub.

To pull the multi-architecture image:

```bash
docker pull yourusername/visitorpass:latest
```

The appropriate image for your architecture will be automatically selected.

### Environment Variables Configuration

VisitorPass supports extensive configuration through environment variables, making it easy to deploy in different environments without modifying code.

#### Setup Steps:

1. **Create your environment file**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit with your specific settings
   nano .env
   ```

2. **Available Configuration Options**:

   <details>
   <summary>Click to see all available environment variables</summary>

   ```
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
   CSRF_TRUSTED_ORIGINS=https://your-domain.com

   # Database Settings
   USE_SQLITE=False
   DATABASE_URL=postgresql://username:password@db:5432/dbname

   # PostgreSQL Settings
   POSTGRES_USER=username
   POSTGRES_PASSWORD=password
   POSTGRES_DB=dbname
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # Email Settings
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-password
   EMAIL_USE_TLS=True

   # Admin User Settings
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=adminpass
   ADMIN_EMAIL=admin@example.com
   ```
   </details>

3. **Run with environment variables**:
   ```bash
   # Using Docker Compose (recommended)
   docker-compose up -d
   
   # Or with Docker run
   docker run -p 8000:8000 --env-file .env visitorpass
   ```

4. **Override specific variables at runtime**:
   ```bash
   # Override admin credentials
   ADMIN_USERNAME=superadmin ADMIN_PASSWORD=securepass docker-compose up -d
   ```

5. **Different database configurations**:
   ```bash
   # Use SQLite
   docker-compose up -d web-sqlite
   
   # Use PostgreSQL
   docker-compose up -d web-postgres db
   ```

#### Benefits:

- **Security**: Sensitive information is kept out of your codebase
- **Flexibility**: Easy to configure for different environments
- **Maintainability**: All configuration in one place
- **Portability**: Works across different machines and platforms

</details>

<details>
<summary><b>Traditional Web Server (WSGI)</b></summary>

For deployment with Gunicorn and Nginx:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn visitorpass.wsgi:application --bind 0.0.0.0:8000
```

Configure Nginx to proxy requests to Gunicorn.
</details>

<details>
<summary><b>Cloud Platforms</b></summary>

The application can be deployed to various cloud platforms such as:
- AWS Elastic Beanstalk
- Google App Engine
- Microsoft Azure App Service
- Heroku

Follow the specific deployment instructions for your chosen platform.
</details>


## 📞 Contact

<div align="center">
  <a href="https://github.com/christopherece"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="mailto:chris.ancheta@topitsolutions.co.nz"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://www.linkedin.com/in/christopherece/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
</div>

<div align="center">
  <p>Developed by <b>Christopher Ancheta | TopITSolutions.co.nz</b></p>
  <p> 2025 All Rights Reserved</p>
</div>
