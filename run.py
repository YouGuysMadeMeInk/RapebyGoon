# run.py - American Truck Simulator "Rape" Mod Utility

import time
import json
import random
from pathlib import Path

# Simulated path to ATS telemetry data (not real)
TELEMETRY_FILE = Path("C:/Users/YourUser/Documents/ATS/telemetry_data.json")

def load_telemetry():
    """
    Simulate loading telemetry data from ATS.
    """
    if not TELEMETRY_FILE.exists():
        print("[!] Telemetry file not found. Launch ATS first.")
        return None

    print("[*] Reading telemetry data...")
    try:
        with open(TELEMETRY_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[!] Failed to read telemetry: {e}")
        return None

def apply_mod_effects(data):
    """
    Apply a mod effect like adjusting fuel efficiency or weight.
    """
    print("[*] Applying custom 'rape' mod...")
    truck = data.get("truck", {})
    fuel = truck.get("fuel", 100)
    cargo_weight = truck.get("cargo_weight", 0)

    # Mod: Boost fuel efficiency and reduce cargo weight
    modded_fuel = round(fuel * 1.2, 2)
    modded_weight = max(0, cargo_weight - 500)

    print(f"[+] Fuel boosted: {fuel} → {modded_fuel} liters")
    print(f"[+] Cargo lightened: {cargo_weight}kg → {modded_weight}kg")

    # Return modified data
    return {
        "modded_fuel": modded_fuel,
        "modded_cargo_weight": modded_weight
    }

def main():
    print("=== ATS 'Rape' Mod Utility ===")
    time.sleep(1)
    data = load_telemetry()
    if data:
        results = apply_mod_effects(data)
        print("[*] Mod application complete.")
        print(json.dumps(results, indent=4))
    else:
        print("[x] Could not load telemetry data.")

if __name__ == "__main__":
    main()
