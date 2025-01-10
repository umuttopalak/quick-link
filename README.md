# Quick Link - URL Shortener

A modern URL shortener application built with Flask, supporting multiple languages and user authentication.

## Features

- URL shortening functionality
- User authentication (login/register)
- Multi-language support (English and Turkish)
- Click tracking for shortened URLs
- Responsive design
- Docker support

## Tech Stack

- Python 3.9
- Flask
- SQLAlchemy
- Flask-Login for authentication
- Flask-Babel for internationalization
- SQLite database (configurable to other databases)
- Docker

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd quick-link
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create .env file):
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///urls.db  # or your database URL
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Docker Deployment

Build and run the application using Docker:

```bash
docker build -t quick-link .
docker run -p 3000:3000 quick-link
```

## Docker-Compose Deployment

Build and run the application using Docker-Compose:

```bash
docker compose up --build
```

## Internationalization

The application supports English and Turkish languages. To compile translation files:

```bash
pybabel compile -d app/translations
```

To extract new strings for translation:

```bash
pybabel extract -F babel.cfg -o messages.pot .
```

## License

MIT License. See [LICENSE](LICENSE) for more information.