# Phoenix Core AI Engine - Background Execution Logic
# PCS-AI | Red/Blue Theme | Self-Healing | Offline/Online Clone Deployment

import json
import time
import random
import os
import threading
from datetime import datetime

# ===================================================================
# 1. CONFIGURATION & FILE PATHS
# ===================================================================

SYSTEM_HEALTH_FILE = "system_health.json"
LOG_FILE = "phoenix_core_engine.log"

# Damage thresholds
DAMAGE_THRESHOLD = 1.0          # 1% damage triggers clone extraction
EMERGENCY_THRESHOLD = 20.0      # 20% damage triggers emergency mode
CRITICAL_THRESHOLD = 30.0       # 30% damage forces offline backup mode

# Healing parameters
PASSIVE_HEAL_RATE = 1.5         # Passive healing per cycle
POWER_INJECTION_FACTOR = 1.2    # Power injection multiplier
CLONE_HEAL_FACTOR = 1.5         # Clone deployment healing multiplier

# Simulation intervals (seconds)
MONITOR_INTERVAL = 5            # How often to check system health
ANOMALY_PROBABILITY = 0.4       # 40% chance of anomaly per cycle

# ===================================================================
# 2. SIMULATED DEVICES (Critical Infrastructure)
# ===================================================================

DEVICES = [
    {"id": "bank_servers", "name": "Banking Servers", "critical": True, "health": 100},
    {"id": "aviation", "name": "Aviation Systems", "critical": True, "health": 100},
    {"id": "medical", "name": "Medical Infrastructure", "critical": True, "health": 100},
    {"id": "marine", "name": "Marine Navigation", "critical": False, "health": 100},
    {"id": "power_grid", "name": "Power Grid", "critical": True, "health": 100},
    {"id": "telecom", "name": "Telecom Network", "critical": True, "health": 100},
    {"id": "water_supply", "name": "Water Supply Systems", "critical": True, "health": 100},
    {"id": "emergency_services", "name": "Emergency Services", "critical": False, "health": 100}
]

# ===================================================================
# 3. LOGGING & TERMINAL STYLING
# ===================================================================

def log_message(message, level="INFO"):
    """Write log to file and print with color coding"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    # Write to log file
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")
    
    # Terminal output with colors
    if level == "CRITICAL":
        print(f"\033[91m{log_entry}\033[0m")      # Red
    elif level == "HEALING":
        print(f"\033[92m{log_entry}\033[0m")      # Green
    elif level == "EMERGENCY":
        print(f"\033[93m{log_entry}\033[0m")      # Yellow
    else:
        print(f"\033[94m{log_entry}\033[0m")      # Blue

# ===================================================================
# 4. FILE MANAGEMENT FUNCTIONS
# ===================================================================

def load_system_health():
    """Load current system health from JSON file"""
    if os.path.exists(SYSTEM_HEALTH_FILE):
        with open(SYSTEM_HEALTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Create default health status
        default_health = {
            "system_health": 100.0,
            "power_injection": 0.0,
            "clone_status": "IDLE",
            "emergency_mode": False,
            "offline_mode": False,
            "healing_pulses": 0,
            "healed_cells": 0,
            "last_updated": datetime.now().isoformat(),
            "devices": DEVICES
        }
        save_system_health(default_health)
        return default_health

def save_system_health(health_data):
    """Save current system health to JSON file (shared with frontend)"""
    health_data["last_updated"] = datetime.now().isoformat()
    with open(SYSTEM_HEALTH_FILE, "w", encoding="utf-8") as f:
        json.dump(health_data, f, indent=2)

# ===================================================================
# 5. CORE ENGINE FUNCTIONS
# ===================================================================

def power_injection(health_data, damage_percent):
    """Simulate emergency power injection to damaged processors"""
    current_power = health_data.get("power_injection", 0)
    # Inject power proportional to damage (max 100%)
    power_increase = damage_percent * POWER_INJECTION_FACTOR
    new_power = min(100, current_power + power_increase)
    health_data["power_injection"] = new_power
    
    log_message(
        f"⚡ POWER INJECTION: +{power_increase:.1f}% | Total: {new_power:.1f}%",
        "HEALING"
    )
    return health_data

def clone_extraction_and_deployment(health_data, damage_percent):
    """Extract safe circle master copy and deploy offline clone"""
    log_message(
        f"🔬 CLONE EXTRACTION initiated (Damage: {damage_percent:.1f}%)",
        "HEALING"
    )
    health_data["clone_status"] = "EXTRACTING"
    save_system_health(health_data)
    
    # Simulate extraction time with progress
    extraction_progress = 0
    extraction_steps = 0
    while extraction_progress < 100 and extraction_steps < 10:
        time.sleep(0.1)
        extraction_progress += random.randint(10, 25)
        extraction_progress = min(100, extraction_progress)
        extraction_steps += 1
        if extraction_steps % 3 == 0:
            log_message(f"📀 Clone extraction progress: {extraction_progress:.0f}%", "HEALING")
    
    health_data["clone_status"] = "DEPLOYED"
    save_system_health(health_data)
    log_message(f"✅ CLONE DEPLOYED: Safe circle master copy restored to damaged sectors", "HEALING")
    
    # Begin healing after clone deployment
    healing_amount = min(100, damage_percent * CLONE_HEAL_FACTOR)
    health_data["system_health"] = min(100, health_data["system_health"] + healing_amount)
    health_data["healing_pulses"] = health_data.get("healing_pulses", 0) + 1
    health_data["healed_cells"] = health_data.get("healed_cells", 0) + int(healing_amount * 10)
    
    log_message(f"🏥 PHOENIX HEALING: +{healing_amount:.1f}% system recovery", "HEALING")
    return health_data

def emergency_mode_activation(health_data, damage_percent):
    """Activate emergency mode when damage exceeds threshold"""
    if damage_percent >= EMERGENCY_THRESHOLD and not health_data.get("emergency_mode", False):
        health_data["emergency_mode"] = True
        operational_capacity = max(50, 100 - damage_percent)
        log_message(
            f"🚨 EMERGENCY MODE ACTIVATED! Damage: {damage_percent:.1f}% | "
            f"Operational Capacity: {operational_capacity:.0f}%",
            "EMERGENCY"
        )
        
        # List critical devices running at reduced capacity
        critical_devices = [d["name"] for d in DEVICES if d.get("critical", False)]
        log_message(
            f"⚠️ Critical systems running at reduced capacity: {', '.join(critical_devices[:5])}",
            "EMERGENCY"
        )
        
        # If damage > CRITICAL_THRESHOLD, switch to full offline backup
        if damage_percent >= CRITICAL_THRESHOLD:
            log_message(
                f"📡 OFFLINE BACKUP MODE: All critical operations switched to local safe copies",
                "EMERGENCY"
            )
            health_data["offline_mode"] = True
    
    elif damage_percent < EMERGENCY_THRESHOLD and health_data.get("emergency_mode", False):
        health_data["emergency_mode"] = False
        health_data["offline_mode"] = False
        log_message(f"✅ Emergency mode deactivated. Systems returning to normal.", "HEALING")
    
    return health_data

def update_device_health(health_data, damage_percent):
    """Apply damage to individual devices"""
    # Select random device to damage
    damaged_device = random.choice(DEVICES)
    device_damage = damage_percent * random.uniform(0.5, 1.2)
    damaged_device["health"] = max(0, damaged_device["health"] - device_damage)
    
    log_message(
        f"⚠️ DEVICE DAMAGE: {damaged_device['name']} lost {device_damage:.1f}% health "
        f"(Now: {damaged_device['health']:.1f}%)",
        "CRITICAL"
    )
    
    # Emergency alert for critical devices below 30%
    if damaged_device["critical"] and damaged_device["health"] < 30:
        log_message(
            f"🔴 CRITICAL ALERT: {damaged_device['name']} below 30%! "
            f"Initiating emergency protocols.",
            "EMERGENCY"
        )
    
    # Trigger clone deployment if critical device is severely damaged
    if damaged_device["critical"] and damaged_device["health"] < 20:
        log_message(
            f"🔄 Automatic clone deployment triggered for {damaged_device['name']}",
            "HEALING"
        )
        health_data["clone_status"] = "EXTRACTING"
    
    health_data["devices"] = DEVICES
    return health_data

def passive_healing(health_data):
    """Apply passive healing over time"""
    if health_data["system_health"] < 100 and health_data["system_health"] > 0:
        passive_heal = random.uniform(0.5, PASSIVE_HEAL_RATE)
        new_health = min(100, health_data["system_health"] + passive_heal)
        old_health = health_data["system_health"]
        health_data["system_health"] = new_health
        
        log_message(
            f"🌿 PASSIVE REGENERATION: +{passive_heal:.1f}% | "
            f"Health: {new_health:.1f}%",
            "HEALING"
        )
        
        # Gradual reduction of power injection
        if health_data.get("power_injection", 0) > 0:
            power_reduction = passive_heal * 0.3
            health_data["power_injection"] = max(0, health_data["power_injection"] - power_reduction)
    
    return health_data

def check_anomaly_and_respond(health_data):
    """Main anomaly detection and response logic"""
    current_health = health_data.get("system_health", 100)
    anomaly_detected = random.random() < ANOMALY_PROBABILITY
    
    if not anomaly_detected or current_health <= 0:
        return health_data
    
    # Generate random damage (0.5% to 9%)
    damage = random.uniform(0.5, 9.0)
    new_health = max(0, current_health - damage)
    actual_damage = current_health - new_health
    health_data["system_health"] = new_health
    
    log_message(
        f"⚠️ ANOMALY DETECTED! Damage: -{actual_damage:.1f}% | "
        f"System Health: {new_health:.1f}%",
        "CRITICAL"
    )
    
    # Apply damage to individual devices
    health_data = update_device_health(health_data, actual_damage)
    
    # CRITICAL: If damage >= threshold -> Trigger Self-Healing Protocols
    if actual_damage >= DAMAGE_THRESHOLD or new_health <= 99:
        log_message(
            f"🔔 THRESHOLD REACHED (>=1%) - Activating Self-Healing Protocols",
            "HEALING"
        )
        
        # 1. Power Injection
        health_data = power_injection(health_data, actual_damage)
        
        # 2. Clone Extraction & Deployment
        health_data = clone_extraction_and_deployment(health_data, actual_damage)
        
        # 3. Update system health after healing
        if health_data["system_health"] > new_health:
            log_message(
                f"✨ Healing applied: New system health = {health_data['system_health']:.1f}%",
                "HEALING"
            )
    
    # Check for Emergency Mode (20-30% damage)
    damage_percent = 100 - health_data["system_health"]
    health_data = emergency_mode_activation(health_data, damage_percent)
    
    return health_data

# ===================================================================
# 6. MAIN BACKGROUND LOOP
# ===================================================================

def background_monitor():
    """Main background loop that monitors system and triggers actions"""
    log_message("=" * 60, "INFO")
    log_message("🔥 PHOENIX CORE AI ENGINE STARTED (Background Execution)", "HEALING")
    log_message(f"⚡ Monitoring system for anomalies (Threshold: {DAMAGE_THRESHOLD}% damage)", "INFO")
    log_message(f"🛡️ Emergency Mode Ready at {EMERGENCY_THRESHOLD}% | Offline Backup at {CRITICAL_THRESHOLD}%", "INFO")
    log_message(f"📊 Monitoring {len(DEVICES)} critical infrastructure devices", "INFO")
    log_message("=" * 60, "INFO")
    
    cycle_count = 0
    
    while True:
        try:
            # Load current system health
            health_data = load_system_health()
            
            # Detect and respond to anomalies
            health_data = check_anomaly_and_respond(health_data)
            
            # Apply passive healing
            health_data = passive_healing(health_data)
            
            # Save updated health data
            save_system_health(health_data)
            
            cycle_count += 1
            if cycle_count % 10 == 0:
                current_health = health_data.get("system_health", 100)
                log_message(
                    f"📊 STATUS UPDATE: System Health = {current_health:.1f}% | "
                    f"Power Injection = {health_data.get('power_injection', 0):.1f}% | "
                    f"Mode = {'EMERGENCY' if health_data.get('emergency_mode') else 'NORMAL'}",
                    "INFO"
                )
            
            # Wait before next cycle
            time.sleep(MONITOR_INTERVAL)
            
        except KeyboardInterrupt:
            log_message("🛑 Phoenix Core AI Engine stopped by user", "INFO")
            break
        except Exception as e:
            log_message(f"❌ ERROR: {str(e)}", "CRITICAL")
            time.sleep(5)

# ===================================================================
# 7. ENGINE STATUS FUNCTIONS (For external calls)
# ===================================================================

def get_engine_status():
    """Return current engine status for API endpoints"""
    health_data = load_system_health()
    return {
        "status": "running",
        "system_health": health_data.get("system_health", 100),
        "power_injection": health_data.get("power_injection", 0),
        "clone_status": health_data.get("clone_status", "IDLE"),
        "emergency_mode": health_data.get("emergency_mode", False),
        "healing_pulses": health_data.get("healing_pulses", 0),
        "healed_cells": health_data.get("healed_cells", 0),
        "last_updated": health_data.get("last_updated", ""),
        "devices_count": len(health_data.get("devices", []))
    }

def reset_engine():
    """Reset the entire engine to default state"""
    default_health = {
        "system_health": 100.0,
        "power_injection": 0.0,
        "clone_status": "IDLE",
        "emergency_mode": False,
        "offline_mode": False,
        "healing_pulses": 0,
        "healed_cells": 0,
        "last_updated": datetime.now().isoformat(),
        "devices": [dict(d) for d in DEVICES]  # Deep copy
    }
    # Reset device health to 100
    for device in default_health["devices"]:
        device["health"] = 100
    
    save_system_health(default_health)
    log_message("🔄 ENGINE RESET: All systems restored to 100% health", "HEALING")
    return default_health

def manual_heal(device_id=None):
    """Manually trigger healing for a specific device or all devices"""
    health_data = load_system_health()
    
    if device_id:
        # Find and heal specific device
        for device in health_data.get("devices", []):
            if device["id"] == device_id:
                old_health = device["health"]
                device["health"] = min(100, device["health"] + 25)
                log_message(
                    f"💊 MANUAL HEAL: {device['name']} healed from {old_health}% to {device['health']}%",
                    "HEALING"
                )
                break
    else:
        # Heal all devices
        for device in health_data.get("devices", []):
            device["health"] = min(100, device["health"] + 15)
        log_message(f"💊 MANUAL HEAL: All devices partially restored", "HEALING")
    
    # Recalculate system health
    total_health = sum(d["health"] for d in health_data.get("devices", []))
    device_count = len(health_data.get("devices", []))
    health_data["system_health"] = total_health / device_count if device_count > 0 else 100
    
    save_system_health(health_data)
    return health_data

# ===================================================================
# 8. ENTRY POINT (For standalone execution)
# ===================================================================

if __name__ == "__main__":
    try:
        background_monitor()
    except KeyboardInterrupt:
        print("\n\033[94m🛑 Phoenix Core AI Engine Terminated\033[0m")