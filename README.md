# Quick Link - URL Shortener

A modern URL shortener application built with Flask, supporting multiple languages and user authentication with Firebase/Google Sign-In.

## Features

- URL shortening functionality
- User authentication (login/register)
- Google Sign-In support via Firebase
- Multi-language support (English and Turkish)
- Click tracking for shortened URLs
- Responsive design
- Docker support

## Tech Stack

- Python 3.9
- Flask
- SQLAlchemy
- Flask-Login for authentication
- Firebase for Google authentication
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

4. Firebase Configuration:
   - Create a new project in [Firebase Console](https://console.firebase.google.com/)
   - Set up Authentication and enable Google Sign-In
   - Create a web app and get your Firebase configuration
   - Download service account JSON file and save as `firebase-credentials.json` in project root

5. Set up environment variables (create .env file):
```bash
# Application Settings
SECRET_KEY=your-secret-key-here
BABEL_DEFAULT_LOCALE=tr
TIMEZONE=Europe/Istanbul

# Database Settings
DATABASE_URL=sqlite:///urls.db

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_WEB_API_KEY=your-firebase-web-api-key
FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-app.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=1:your-app-id:web:your-app-hash
FIREBASE_MEASUREMENT_ID=G-MEASUREMENT-ID
```

6. Initialize the database:
```bash
flask db upgrade
```

7. Run the application:
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

## Production Deployment

### Firebase Credentials in Production

For security reasons, `firebase-credentials.json` should never be committed to your repository. In production environments, there are two recommended approaches:

1. **Environment Variable (Recommended):**
   - Convert your `firebase-credentials.json` file to a string:
     ```bash
     cat firebase-credentials.json | jq -c
     ```
   - Set this entire JSON string as the `FIREBASE_CREDENTIALS_JSON` environment variable in your production environment
   - The application is configured to read credentials from this environment variable first

2. **Secure File Upload:**
   - Securely upload the `firebase-credentials.json` file to your production server (outside of the repository)
   - Set the `FIREBASE_CREDENTIALS_PATH` environment variable to point to this file location

For hosting platforms (Heroku, Vercel, etc.), use their built-in environment variable configuration systems through their dashboard or CLI.

## License

MIT License. See [LICENSE](LICENSE) for more information.