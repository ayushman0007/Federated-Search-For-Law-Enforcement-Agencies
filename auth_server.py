from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # A simple index route so you know the server is running.
    return "Auth server is running! To simulate authorization, go to /authorize?user=testuser."

@app.route('/authorize')
def authorize():
    user = request.args.get('user')
    print(f"✅ Received /authorize request for user: {user}")
    # Use a simulated code that begins with "mock" so the client knows to bypass real token fetching.
    return redirect(f"http://127.0.0.1:8000/callback?code=mockcode123&user={user}")

if __name__ == '__main__':
    print("✅ Running auth server on http://127.0.0.1:5000")
    app.run(port=5000)