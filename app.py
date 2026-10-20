#!/usr/bin/env python3
"""Block Blast server. No dependencies: only the Python standard library.

Usage:
    python app.py              # http://localhost:8000
    python app.py 5000         # custom port

OBS Browser Source URL: http://localhost:8000/?overlay=1
"""
import http.server
import os
import socketserver
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Block Blast: http://localhost:{PORT}")
        print(f"OBS overlay: http://localhost:{PORT}/?overlay=1")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nBye!")
