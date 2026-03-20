from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database setup: Creates security.db in your project folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'security.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for Portfolio Persistence
class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.String(20))
    status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.now)

# Global variable to track the alarm state (Red LED/Buzzer control)
alarm_active = False

@app.route('/')
def index():
    # Fetch all logs for the Dashboard display, newest first
    logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).all()
    return render_template('logs.html', logs=logs, alarm=alarm_active)

@app.route('/scan', methods=['POST', 'GET'])
def scan():
    global alarm_active
    tag = None

    # 1. Try to get data from a POST request (JSON)
    if request.is_json:
        data = request.get_json()
        tag = data.get('tag_id')
    
    # 2. Fallback: Try to get data from a GET request (URL parameters)
    # This ensures communication if the network blocks POST payloads
    if not tag:
        tag = request.args.get('tag_id')

    # If no tag is found in the request
    if not tag:
        return jsonify({"error": "No Tag ID provided"}), 400

    # Business Logic: Card vs Tag
    # Your Card UID: 89227406 (Access Granted)
    # Your Tag UID: B5722D06 (Access Denied)
    if tag == "89227406":
        status = "GRANTED"
        alarm_active = False # Reset alarm if owner scans
    elif tag == "B5722D06":
        status = "DENIED"
        alarm_active = True  # Trigger alarm for the Tag
    else:
        status = "DENIED (UNKNOWN)"
        alarm_active = True  # Trigger alarm for any other ID

    # Save to SQLite Database
    new_log = AccessLog(tag_id=tag, status=status)
    db.session.add(new_log)
    db.session.commit()

    print(f"[*] Access attempt: {tag} - Result: {status} - Alarm: {alarm_active}")
    
    return jsonify({
        "status": status, 
        "alarm": alarm_active,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@app.route('/dismiss', methods=['POST'])
def dismiss():
    global alarm_active
    alarm_active = False 
    print("[!] Administrative Override: Alarm Dismissed via Dashboard.")
    return redirect(url_for('index'))

@app.route('/status', methods=['GET'])
def get_status():
    # The ESP32 calls this every 2 seconds via syncAlarmStatus()
    return jsonify({"alarm_active": alarm_active})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    
    # host='0.0.0.0' binds to both your phone's IP and your 112.185 bridge IP
    print("\n--- SERVER STARTING ---")
    print("Dashboard: http://localhost:5000")
    print(f"Bridge Endpoint: http://10.112.185.239:5000")
    app.run(host='0.0.0.0', port=5000)