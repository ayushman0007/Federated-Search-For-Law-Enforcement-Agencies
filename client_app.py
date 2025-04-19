from flask import Flask, redirect, session, url_for, request
from flask import render_template_string
import os
import pathlib
import google.auth.transport.requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 🔒 Replace with a secure key in production

# Allow HTTP during development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Real Google OAuth credentials
GOOGLE_CLIENT_ID = "646479140943-ghkc0ckbrpanm4bbt9r4l0l1rrki7p1g.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRETS_FILE = "client_secrets.json"

@app.route('/')
def index():
    if 'email' in session:
        return f"""
        <h2>✅ Welcome, {session['email']}!</h2>
        <a href='/logout'>Logout</a>
        """
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        redirect_uri='http://127.0.0.1:8000/callback'
    )
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Rebuild the flow object with the same state and redirect URI
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=[
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        redirect_uri='http://127.0.0.1:8000/callback'
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()

    # Verify and decode the ID token
    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        request_session,
        GOOGLE_CLIENT_ID
    )

    # Save user's email in the session
    session['email'] = id_info.get('email')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)