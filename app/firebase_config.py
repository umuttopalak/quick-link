import json
import os

import firebase_admin
from firebase_admin import auth, credentials
from google.auth.transport import requests
from google.oauth2 import id_token

from config import Config

# Firebase credentials
firebase_credentials_path = Config.FIREBASE_CREDENTIALS_PATH
firebase_web_api_key = Config.FIREBASE_WEB_API_KEY

# Initialize Firebase Admin SDK
try:
    # Try to use credentials from environment variable first
    firebase_credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
    
    if firebase_credentials_json:
        # Use credentials directly from environment variable
        cred_dict = json.loads(firebase_credentials_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    elif os.path.exists(firebase_credentials_path) and os.path.getsize(firebase_credentials_path) > 5:
        # Fall back to file if available
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
    else:
        # For development/testing without credentials
        print("Using default Firebase initialization without credentials file")
        firebase_admin.initialize_app()
except Exception as e:
    print(f"Firebase initialization error: {e}")
    
def verify_firebase_token(id_token_str):
    """Verify Firebase ID token and return user info"""
    try:
        decoded_token = auth.verify_id_token(id_token_str)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        return None

def verify_google_oauth_token(token):
    """Verify Google OAuth token"""
    try:
        # Verify the token using Google's API
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), firebase_web_api_key)

        # Check if the token is for your app
        if idinfo['aud'] not in [firebase_web_api_key]:
            raise ValueError('Could not verify audience.')
        
        return idinfo
    except ValueError as e:
        # Invalid token
        print(f"Error verifying Google token: {e}")
        return None 

# Provide Firebase configuration for front-end
def get_firebase_config():
    """Return Firebase configuration for front-end use"""
    return {
        'apiKey': Config.FIREBASE_WEB_API_KEY,
        'authDomain': Config.FIREBASE_AUTH_DOMAIN,
        'projectId': Config.FIREBASE_PROJECT_ID,
        'storageBucket': Config.FIREBASE_STORAGE_BUCKET,
        'messagingSenderId': Config.FIREBASE_MESSAGING_SENDER_ID,
        'appId': Config.FIREBASE_APP_ID,
        'measurementId': Config.FIREBASE_MEASUREMENT_ID
    } 