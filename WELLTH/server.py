import os
import json
import random
import string
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

PORT    = 8000
DB_FILE = 'db.json'


def uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


class WellthHTTPRequestHandler(SimpleHTTPRequestHandler):

    # ── DB helpers ──────────────────────────────────────────────────────────
    def read_db(self):
        blank = {"transactions": [], "mealPlans": [], "workoutRoutines": [], "bookings": []}
        if not os.path.exists(DB_FILE):
            self.write_db(blank)
            return blank
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return blank

    def write_db(self, data):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    # ── Request logging ─────────────────────────────────────────────────────
    def log_message(self, fmt, *args):
        if '/api' in self.path:
            print(f"[{self.log_date_time_string()}] {self.command} {self.path}")

    # ── Read JSON body ───────────────────────────────────────────────────────
    def parse_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return None

    # ── Response helpers ─────────────────────────────────────────────────────
    def json_response(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def err(self, status, msg):
        self.json_response({"error": msg}, status)

    # ── OPTIONS ──────────────────────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    # ── GET ───────────────────────────────────────────────────────────────────
    def do_GET(self):
        parsed = urlparse(self.path)
        p = parsed.path

        if p == '/':
            self.send_response(302)
            self.send_header('Location', '/wellth-home.html')
            self.end_headers()
            return

        if p == '/api/health':
            db = self.read_db()
            self.json_response({
                "status": "ok",
                "counts": {
                    "transactions": len(db.get('transactions', [])),
                    "mealPlans":    len(db.get('mealPlans', [])),
                    "workouts":     len(db.get('workoutRoutines', [])),
                    "bookings":     len(db.get('bookings', []))
                }
            })
        elif p == '/api/budget':
            self.json_response(self.read_db().get('transactions', []))
        elif p == '/api/meals':
            self.json_response(self.read_db().get('mealPlans', []))
        elif p == '/api/meals/summary':
            db   = self.read_db()
            days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            summary = {d: {"total": 0, "count": 0} for d in days}
            for m in db.get('mealPlans', []):
                if m.get('day') in summary:
                    summary[m['day']]['total'] += m.get('calories', 0)
                    summary[m['day']]['count'] += 1
            self.json_response(summary)
        elif p == '/api/workouts':
            self.json_response(self.read_db().get('workoutRoutines', []))
        elif p == '/api/bookings':
            self.json_response(self.read_db().get('bookings', []))
        else:
            super().do_GET()

    # ── POST ─────────────────────────────────────────────────────────────────
    def do_POST(self):
        p    = urlparse(self.path).path
        body = self.parse_body()
        if body is None:
            return self.err(400, 'Invalid JSON body')

        db = self.read_db()

        if p == '/api/budget':
            text, amount, type_val = body.get('text'), body.get('amount'), body.get('type')
            if not text or amount is None or not type_val:
                return self.err(400, 'Missing text, amount, or type')
            item = {
                "id": uid(), "text": text,
                "amount": float(amount), "type": type_val,
                "category": body.get('category', 'neutral'),
                "date": body.get('date', '')
            }
            db.setdefault('transactions', []).append(item)
            self.write_db(db)
            self.json_response(item, 201)

        elif p == '/api/meals':
            day, meal_type, meal_name = body.get('day'), body.get('mealType'), body.get('mealName')
            if not day or not meal_type or not meal_name:
                return self.err(400, 'Missing day, mealType, or mealName')
            item = {
                "id": uid(), "day": day, "mealType": meal_type,
                "mealName": meal_name,
                "calories": int(body.get('calories', 0)),
                "tags": body.get('tags', [])
            }
            db.setdefault('mealPlans', []).append(item)
            self.write_db(db)
            self.json_response(item, 201)

        elif p == '/api/workouts':
            name, exercises = body.get('routineName'), body.get('exercises')
            if not name or not exercises:
                return self.err(400, 'Missing routineName or exercises')
            item = {
                "id": uid(), "routineName": name,
                "duration": body.get('duration', '30 mins'),
                "difficulty": body.get('difficulty', 'Intermediate'),
                "calories": int(body.get('calories', 0)),
                "exercises": exercises
            }
            db.setdefault('workoutRoutines', []).append(item)
            self.write_db(db)
            self.json_response(item, 201)

        elif p == '/api/bookings':
            pro, date, time = body.get('professionalName'), body.get('date'), body.get('time')
            if not pro or not date or not time:
                return self.err(400, 'Missing professionalName, date, or time')
            item = {
                "id": uid(), "professionalName": pro,
                "date": date, "time": time,
                "notes": body.get('notes', ''),
                "status": "confirmed"
            }
            db.setdefault('bookings', []).append(item)
            self.write_db(db)
            self.json_response(item, 201)
        else:
            self.err(404, 'API endpoint not found')

    # ── DELETE ────────────────────────────────────────────────────────────────
    def do_DELETE(self):
        p  = urlparse(self.path).path
        db = self.read_db()

        # Match /api/<collection>/<id>
        parts = p.strip('/').split('/')   # ['api', 'budget', '<id>']
        if len(parts) != 3 or parts[0] != 'api':
            return self.err(400, 'Invalid DELETE path')

        collection_map = {
            'budget':   'transactions',
            'meals':    'mealPlans',
            'workouts': 'workoutRoutines',
            'bookings': 'bookings'
        }
        key = collection_map.get(parts[1])
        if not key:
            return self.err(404, 'API endpoint not found')

        record_id  = parts[2]
        collection = db.get(key, [])
        idx = next((i for i, x in enumerate(collection) if x.get('id') == record_id), -1)
        if idx == -1:
            return self.err(404, 'Record not found')

        deleted = collection.pop(idx)
        db[key]  = collection
        self.write_db(db)
        self.json_response({"message": "Deleted", "deleted": deleted})


def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, WellthHTTPRequestHandler)
    print("=" * 50)
    print("  WELLTH Python Backend running")
    print(f"  http://localhost:{PORT}")
    print(f"  API health: http://localhost:{PORT}/api/health")
    print("=" * 50)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run()
