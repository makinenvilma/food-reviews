# Blog Web App

A content management platform that allows users to create, edit, and delete blog posts.  
The application includes both a public-facing blog and an admin panel for managing content.  
Built as a full-stack application using Python and Django, it demonstrates skills in web development, database integration, and content management systems.

## Features

- **Create Posts** – Write and publish new blog posts.  
- **Edit & Delete** – Update or remove existing posts.  
- **Admin Panel** – Manage content through a Wagtail-powered dashboard.  
- **Responsive UI** – Works seamlessly on desktop and mobile devices.

## Screenshots

**Blog Post View**  
_Example view of a published blog post._

**Admin Panel**  
_Example view of the Wagtail CMS dashboard._

## Tech Stack

- **Back-end:** Python, Django, Wagtail  
- **Front-end:** HTML, CSS  
- **Database:** (Configured in Django settings – e.g., SQLite/PostgreSQL)  

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blog-web-app.git
   cd blog-web-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**  
   Create a `.env` file in the project root (or configure your settings module):
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the application**
   ```bash
   python manage.py runserver
   ```
   The app will be available at `http://localhost:8000`

## How It Works

- **Django** handles both front-end rendering and back-end logic.  
- **Wagtail** provides a robust admin interface for managing blog content.  
- **HTML & CSS** deliver a clean and responsive layout.  

