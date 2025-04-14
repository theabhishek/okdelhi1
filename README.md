# Reddit Clone

A modern Reddit clone built with Django and Tailwind CSS.

## Features

- User Authentication (Signup/Login/Logout)
- Subreddits (Communities)
- Posts (Text, Link, Image/Video support)
- Voting System
- Comments with nested replies
- Feed with sorting options
- Basic Moderation

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
reddit_clone/
├── core/           # Main app
├── users/          # User authentication
├── subreddits/     # Communities
├── posts/          # Posts and comments
├── static/         # Static files
└── templates/      # HTML templates
``` 