# Reddit Clone Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd reddit-clone
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

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

## Features

1. User Authentication
   - Sign up with email and password
   - Login/Logout functionality
   - User profiles with avatars

2. Subreddits (Communities)
   - Create and browse communities
   - Community pages with description and rules
   - Subscribe to communities

3. Posts
   - Create text, link, and image posts
   - View posts in feed
   - Post details page

4. Voting System
   - Upvote/downvote posts and comments
   - Real-time vote count updates

5. Comments
   - Add and reply to comments
   - Nested comments (threaded view)
   - Upvote/downvote comments

6. Feed
   - Home feed (all communities)
   - Community-specific feeds
   - Sorting options: Hot, New, Top

## Development

1. Create a new app:
```bash
python manage.py startapp app_name
```

2. Create migrations:
```bash
python manage.py makemigrations
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Run tests:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 