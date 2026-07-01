
# PCS-AI Flask Server - Main Application
# All pages connected with authentication and background engine

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import random
import threading
import time
import os

app = Flask(__name__)
app.secret_key = "phoenix_core_secret_key"

HEALTH_FILE = "system_health.json"
USERS_FILE = "users.json"

# ==================== FILE INITIALIZATION ====================

def init_health_file():
    if not os.path.exists(HEALTH_FILE):
        data = {
            "system_health": 100,
            "power_injection": 0,
            "clone_status": "IDLE",
            "emergency_mode": False,
            "offline_mode": False,
            "healing_pulses": 0,
            "healed_cells": 0,
            "devices": []
        }
        with open(HEALTH_FILE, "w") as f:
            json.dump(data, f)

def init_users_file():
    if not os.path.exists(USERS_FILE):
        users = {"admin": {"password": "admin123", "email": "admin@pcs.ai"}}
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

def load_health():
    init_health_file()
    with open(HEALTH_FILE, "r") as f:
        return json.load(f)

def save_health(data):
    with open(HEALTH_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_users():
    init_users_file()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ==================== BACKGROUND ENGINE (Phoenix Core) ====================

def background_engine():
    while True:
        time.sleep(5)
        data = load_health()
        if data["system_health"] > 0:
            damage = random.uniform(0.5, 8)
            data["system_health"] = max(0, data["system_health"] - damage)
            
            if damage >= 1:
                data["power_injection"] = min(100, data["power_injection"] + damage * 1.2)
                data["clone_status"] = "EXTRACTING"
                data["healing_pulses"] += 1
                time.sleep(0.3)
                data["clone_status"] = "DEPLOYED"
                heal = damage * 1.5
                data["system_health"] = min(100, data["system_health"] + heal)
                data["healed_cells"] += int(heal * 10)
            
            if 100 - data["system_health"] >= 20:
                data["emergency_mode"] = True
                data["offline_mode"] = True
            else:
                data["emergency_mode"] = False
                data["offline_mode"] = False
            
            if data["system_health"] < 100 and data["system_health"] > 0:
                data["system_health"] = min(100, data["system_health"] + random.uniform(0.5, 2))
            
            save_health(data)

threading.Thread(target=background_engine, daemon=True).start()

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    return render_template('INDEX.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            session['user'] = username
            return redirect(url_for('biometric_face_gate'))
        return render_template('login.html', error="Please fill in both fields")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()
        if username in users:
            return render_template('REGISTRATION.html', error="Username exists")
        users[username] = {"password": password, "email": email}
        save_users(users)
        return redirect(url_for('login'))
    return render_template('REGISTRATION.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('logout.html')

# ==================== BIOMETRIC FACE GATE ====================

@app.route('/face-gate')
def biometric_face_gate():
    return render_template('AI Biometric Face Gate.html')

# ==================== MAIN DASHBOARD & CORE ====================

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Phoenix Dashboard.html')

@app.route('/phoenix')
def phoenix():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('phoenix-core-unit.html')

# ==================== SECURITY AGENTS ====================

@app.route('/forensic')
def forensic():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('forensic_agent.html')

@app.route('/active-defense')
def active_defense():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('active-defense.html')

@app.route('/evidence-logs')
def evidence_logs():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('evidence-logs.html')

@app.route('/bug-hunter')
def bug_hunter():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('bug-hunter.html')

# ==================== DEVICE MANAGEMENT ====================

@app.route('/network-devices')
def network_devices():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('network-devices.html')

@app.route('/iphone-management')
def iphone_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('iPhone-Management.html')

@app.route('/ipad-management')
def ipad_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('iPad-Management.html')

@app.route('/tablet-management')
def tablet_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Tablet-Management.html')

@app.route('/laptop-pc-management')
def laptop_pc_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Laptop-PC-Management.html')

# ==================== CRITICAL INFRASTRUCTURE ====================

@app.route('/marine-ships')
def marine_ships():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Marine-Ships-System.html')

@app.route('/servers-management')
def servers_management():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Servers-Management.html')

@app.route('/systems-clone')
def systems_clone():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('systems-clone.html')

@app.route('/hardware-unit')
def hardware_unit():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('hardware-unit.html')

# ==================== THREAT INTELLIGENCE ====================

@app.route('/threat-center')
def threat_center():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Threat-Center.html')

@app.route('/ai-threat-analysis')
def ai_threat_analysis():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('AI-Threat-Analysis.html')

@app.route('/dmz-isolation')
def dmz_isolation():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('DMZ-Isolation-Center.html')

# ==================== SECURITY POLICIES ====================

@app.route('/settings-security')
def settings_security():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Settings-Security-Policies.html')

@app.route('/users-roles')
def users_roles():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Users-Roles-Permissions.html')

# ==================== AI & TRAINING ====================

@app.route('/ai-training')
def ai_training():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('AI-Training-Center.html')

# ==================== MONITORING & MAPS ====================

@app.route('/live-attack-map')
def live_attack_map():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Live-Global-Attack-Map.html')

# ==================== CLOUD & API ====================

@app.route('/cloud-security')
def cloud_security():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Cloud-Security.html')

@app.route('/api-sdk')
def api_sdk():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('API-SDK-Center.html')

# ==================== BACKUP & RECOVERY ====================

@app.route('/backup-disaster')
def backup_disaster():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Backup-Disaster-Recovery.html')

@app.route('/system-health')
def system_health():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('System-Health-Center.html')

# ==================== VPN & HARDWARE RENEWAL ====================

@app.route('/vpn-gateway')
def vpn_gateway():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('vpn-gateway.html')

@app.route('/hardware-renewal')
def hardware_renewal():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('hardware-renewal.html')

@app.route('/systems-clone-v2')
def systems_clone_v2():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('systems-clone-v2.html')

# ==================== 🔐 SECRET & HIDDEN PAGES (3 Pages) ====================

# 1. ELITE ALERT - Intercept page that appears when hacker opens the decoy file
@app.route('/elite-alert')
def elite_alert():
    """
    Elite Alert Page - Appears when honeypot is triggered
    Silent alert with intelligent guidance
    Access: /elite-alert (no authentication - appears to the hacker)
    """
    return render_template('Elite Alert & Guidance Page.html')


# 2. SHADOW DASHBOARD - Ultra secret room (requires secret key)
@app.route('/shadow-dashboard')
def shadow_dashboard():
    """
    Hidden Shadow Dashboard - Classified Forensics Intelligence
    Access: /shadow-dashboard?key=phoenix-secret-key-2024
    Only Batool, Fatma, and the third authorized person can access
    """
    secret_key = request.args.get('key')
    # Secret key required - only authorized people know it
    if secret_key != 'phoenix-secret-key-2024':
        return redirect(url_for('index'))
    return render_template('The Hidden Shadow Dashboard.html')


# 3. CYBER DECEPTION VAULT - QR Code + Dual Authentication vault
@app.route('/cyber-vault')
def cyber_vault():
    """
    Cyber Deception Vault - QR Code Dual Auth & Hacker Forensics
    Access: /cyber-vault (requires login first)
    Dual authentication required (Batool + Fatma QR scan)
    """
    # Check if user is logged in first
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Cyber-Deception-Vault.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/health')
def api_health():
    return jsonify(load_health())

@app.route('/api/reset')
def api_reset():
    data = load_health()
    data["system_health"] = 100
    data["power_injection"] = 0
    data["clone_status"] = "IDLE"
    data["emergency_mode"] = False
    data["offline_mode"] = False
    save_health(data)
    return jsonify({"status": "success", "message": "System reset to 100%"})

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    init_health_file()
    init_users_file()
    print("=" * 70)
    print("🔥 PCS-AI PHOENIX CORE SERVER STARTED")
    print("=" * 70)
    print("📍 Main URL: http://127.0.0.1:5000")
    print("📍 Login: http://127.0.0.1:5000/login")
    print("📍 Face Gate: http://127.0.0.1:5000/face-gate")
    print("📍 Dashboard: http://127.0.0.1:5000/dashboard")
    print("-" * 70)
    print("🔐 SECRET PAGES (Authorized Access Only):")
    print("   1. Elite Alert: /elite-alert")
    print("   2. Shadow Dashboard: /shadow-dashboard?key=phoenix-secret-key-2024")
    print("   3. Cyber Deception Vault: /cyber-vault")
    print("-" * 70)
    print("📊 TOTAL PAGES LOADED: 38 Pages")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)