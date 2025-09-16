from flask import Flask, request
import datetime
import os

app = Flask(__name__)
LOG_FILE = "honeypot.log"
ALL_REQ_FILE = "all_requests.log"

# Création du fichier si non existant
for f in [LOG_FILE, ALL_REQ_FILE]:
    if not os.path.exists(f):
        open(f, 'w').close()

def log_attack(attack_type, payload, req):
    with open(LOG_FILE, "a") as f:
        f.write(
            f"[{datetime.datetime.now()}] {attack_type} | "
            f"Payload: {payload} | "
            f"IP: {req.remote_addr} | "
            f"UA: {req.headers.get('User-Agent')}\n"
        )

def log_all(req):
    with open(ALL_REQ_FILE, "a") as f:
        f.write(
            f"[{datetime.datetime.now()}] {req.method} {req.path} | "
            f"Data: {req.values.to_dict()} | "
            f"IP: {req.remote_addr} | "
            f"UA: {req.headers.get('User-Agent')} | "
            f"Referer: {req.headers.get('Referer')} | "
            f"Host: {req.headers.get('Host')} | "
            f"Cookies: {req.headers.get('Cookie')}\n"
        )

@app.before_request
def before_request():
    log_all(request)  # Log toutes les requêtes

# 1. Fake login page (Bruteforce)
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/admin", methods=["GET", "POST"])
@app.route("/dashboard", methods=["GET", "POST"])
@app.route("/wp-login.php", methods=["GET", "POST"])
@app.route("/phpmyadmin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        creds = request.form.to_dict()
        log_attack("Bruteforce / Credential Attempt", creds, request)
        return """
        <h2 style="color:red;">Invalid credentials</h2>
        <a href="/">Try again</a>
        """
    return """
    <html>
    <head>
    <title>Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); width: 300px; }
        h1 { margin-bottom: 24px; color: #333; text-align:center; }
        input { width: 100%; padding: 10px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        a { text-decoration: none; color: #007bff; display: block; text-align:center; margin-top: 10px; }
    </style>
    </head>
    <body>
        <div class="login-box">
            <h1>Admin Panel</h1>
            <form method="POST">
                <input name="user" placeholder="Username">
                <input name="pass" type="password" placeholder="Password">
                <button>Login</button>
            </form>
        </div>
    </body>
    </html>
    """

# 2. Fake search (SQLi)
@app.route("/search")
def search():
    query = request.args.get("q", "")
    if any(x in query.lower() for x in ["union", "select", "drop", "--", "' or"]):
        log_attack("SQL Injection", query, request)
    return f"<h3>Results for '{query}'</h3>"

# 3. Fake profile (XSS)
@app.route("/profile")
def profile():
    name = request.args.get("name", "guest")
    if "<script" in name.lower() or "onerror=" in name.lower():
        log_attack("XSS", name, request)
    return f"<h1>Welcome {name}</h1>"

# 4. Fake ping / server status (Command Injection / RFI)
@app.route("/ping")
@app.route("/status")
def ping():
    host = request.args.get("host", "")
    dangerous = [";", "&&", "|", "wget", "curl", "http://", "https://"]
    if any(x in host.lower() for x in dangerous):
        log_attack("Command Injection / RFI", host, request)
    return f"Pinging {host}..."

if __name__ == "__main__":
    print(" Webserver running on http://0.0.0.0:80")
    app.run(host="0.0.0.0", port=80)
