"""
Mock Local Web Server for 100% Offline, Deterministic UI Testing.

Serves standard test pages replicating demo authentication flows (The Internet):
- Home page (/)
- Form authentication login (/login)
- Authenticated dashboard (/secure)
- Logout flow (/logout)
"""

import http.server
import threading
import urllib.parse
from typing import Optional

HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Internet</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #1e293b; }
        .heading { font-size: 2rem; color: #0f172a; }
        a { color: #2563eb; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1 class="heading">Welcome to the-internet</h1>
    <h2>Available Examples</h2>
    <ul>
        <li><a href="/login">Form Authentication</a></li>
        <li><a href="/checkboxes">Checkboxes</a></li>
        <li><a href="/add_remove_elements/">Add/Remove Elements</a></li>
    </ul>
</body>
</html>
"""

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login Page</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #1e293b; }
        .flash { padding: 12px 20px; border-radius: 6px; margin-bottom: 20px; font-weight: 500; }
        .flash.success { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .flash.error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 300px; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 4px; }
        button { background: #2563eb; color: white; padding: 10px 18px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #1d4ed8; }
        .button.radius { background: #2563eb; }
    </style>
</head>
<body>
    <h2>Login Page</h2>
    <h4 class="subheader">This is where you can log into the secure area.</h4>
    {flash_banner}
    <form id="login" name="login" action="/login" method="POST">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" placeholder="Enter username">
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" name="password" id="password" placeholder="Enter password">
        </div>
        <button class="button radius" type="submit"><i class="fa fa-2x fa-sign-in"></i> Login</button>
    </form>
</body>
</html>
"""

SECURE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure Area</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #1e293b; }
        .flash.success { background: #dcfce7; color: #166534; padding: 12px 20px; border-radius: 6px; margin-bottom: 20px; font-weight: 500; }
        .button { background: #ef4444; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; display: inline-block; }
    </style>
</head>
<body>
    <div id="flash" class="flash success">
        You logged into a secure area!
    </div>
    <h2>Secure Area</h2>
    <h4 class="subheader">Welcome to the Secure Area. When you are done click logout below.</h4>
    <a class="button secondary radius" href="/logout">Logout</a>
</body>
</html>
"""


CHECKBOXES_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Checkboxes</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #1e293b; }
        .heading { font-size: 2rem; color: #0f172a; }
        form { margin-top: 20px; }
        input[type="checkbox"] { margin-right: 8px; margin-bottom: 12px; cursor: pointer; }
    </style>
</head>
<body>
    <h3 class="heading">Checkboxes</h3>
    <form id="checkboxes">
        <input type="checkbox"> checkbox 1<br>
        <input type="checkbox" checked> checkbox 2<br>
    </form>
</body>
</html>
"""

ADD_REMOVE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add/Remove Elements</title>
    <style>
        body { font-family: sans-serif; margin: 40px; background: #f8fafc; color: #1e293b; }
        .heading { font-size: 2rem; color: #0f172a; }
        button { background: #2563eb; color: white; padding: 10px 18px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-bottom: 15px; }
        button:hover { background: #1d4ed8; }
        .added-manually { background: #ef4444; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; display: block; margin-top: 8px; }
        .added-manually:hover { background: #dc2626; }
    </style>
</head>
<body>
    <h3 class="heading">Add/Remove Elements</h3>
    <div class="example">
        <button onclick="addElement()">Add Element</button>
        <div id="elements"></div>
    </div>
    <script>
        function addElement() {
            var container = document.getElementById('elements');
            var btn = document.createElement('button');
            btn.className = 'added-manually';
            btn.innerText = 'Delete';
            btn.onclick = function() {
                this.remove();
            };
            container.appendChild(btn);
        }
    </script>
</body>
</html>
"""


class MockAppRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler simulating the authentication workflows."""

    def log_message(self, format, *args):
        """Suppress default stdout logging to keep test console clean."""
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HOME_HTML.encode("utf-8"))

        elif path in ("/checkboxes", "/checkboxes/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(CHECKBOXES_HTML.encode("utf-8"))

        elif path in ("/add_remove_elements", "/add_remove_elements/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(ADD_REMOVE_HTML.encode("utf-8"))

        elif path == "/login":
            params = urllib.parse.parse_qs(parsed.query)
            error_type = params.get("error", [None])[0]
            flash_html = ""
            if error_type == "invalid_user":
                flash_html = '<div id="flash" class="flash error">Your username is invalid!</div>'
            elif error_type == "invalid_pass":
                flash_html = '<div id="flash" class="flash error">Your password is invalid!</div>'
            elif error_type == "logged_out":
                flash_html = '<div id="flash" class="flash success">You have logged out of the secure area!</div>'

            page_content = LOGIN_HTML.replace("{flash_banner}", flash_html)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page_content.encode("utf-8"))

        elif path == "/secure":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(SECURE_HTML.encode("utf-8"))

        elif path == "/logout":
            self.send_response(302)
            self.send_header("Location", "/login?error=logged_out")
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(length).decode("utf-8")
            fields = urllib.parse.parse_qs(post_data)

            username = fields.get("username", [""])[0]
            password = fields.get("password", [""])[0]

            if username == "tomsmith" and password == "SuperSecretPassword!":
                self.send_response(302)
                self.send_header("Location", "/secure")
                self.end_headers()
            elif username == "tomsmith" and password != "SuperSecretPassword!":
                self.send_response(302)
                self.send_header("Location", "/login?error=invalid_pass")
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header("Location", "/login?error=invalid_user")
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


class MockLocalServer:
    """Threaded HTTP Server for offline testing."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.server: Optional[http.server.HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self) -> str:
        """Start server in background daemon thread and return base URL."""
        self.server = http.server.HTTPServer((self.host, self.port), MockAppRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://{self.host}:{self.port}"

    def stop(self) -> None:
        """Stop server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
