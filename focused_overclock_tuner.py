import requests
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os  # For path expansion

# Configuration for your Bitaxe
BITAXE_IP = "Add your Bitaxe IP"
BASE_URL = f"http://{BITAXE_IP}/api"
START_FREQ = 800  # Focused start
MAX_FREQ = 900    # Focused max
FREQ_STEP = 25    # Frequency increment
START_VOLT = 1250 # Focused voltage start
VOLT_STEP = 25    # Voltage increment
MAX_TEMP = 65     # Increased buffer for ASIC temp
TEST_DURATION = 900  # 15 minutes
PLOT_PATH = "~/bitaxe_automation/focused_run_plot.png"  # Final plot

def set_miner_settings(freq, volt):
    """Send frequency and voltage settings to Bitaxe via API."""
    payload = {"frequency": freq, "coreVoltage": volt, "overclockEnabled": 1}
    try:
        response = requests.patch(f"{BASE_URL}/system", json=payload)
        if response.status_code == 200:
            print(f"Set frequency to {freq} MHz, voltage to {volt} mV")
            return True
        else:
            print(f"Failed to set settings: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error setting settings: {e}")
        return False

def get_miner_status():
    """Get current hash rate, temperatures, and fan speed with retries."""
    for attempt in range(3):
        try:
            response = requests.get(f"{BASE_URL}/system/info")
            data = response.json()
            return {
                "hashrate": data.get("hashRate", 0) / 1000,
                "asic_temp": data.get("temp", 0),
                "vr_temp": data.get("vrTemp", 0),
                "fan_speed": data.get("fanRpm", 0)
            }
        except Exception as e:
            print(f"Error getting status (attempt {attempt+1}): {e}")
            time.sleep(10)
    return None

def test_settings(freq, volt):
    """Test a frequency and voltage combination."""
    if not set_miner_settings(freq, volt):
        return None
    time.sleep(TEST_DURATION)
    status = get_miner_status()
    if not status:
        return None
    if status["asic_temp"] > MAX_TEMP:
        print(f"Unstable: {freq} MHz, {volt} mV, Hashrate {status['hashrate']} TH/s, ASIC {status['asic_temp']}°C, VR {status['vr_temp']}°C")
        return None
    print(f"Stable: {freq} MHz, {volt} mV, Hashrate {status['hashrate']} TH/s, ASIC {status['asic_temp']}°C, VR {status['vr_temp']}°C")
    return status

def main():
    results = []  # List for (freq, volt, hashrate, asic_temp, vr_temp)
    best_settings = {"freq": 800, "volt": 1250, "hashrate": 0}

    print("Starting focused 15-min tests (800-900 MHz / 1250-1300 mV)...")

    for freq in range(START_FREQ, MAX_FREQ + 1, FREQ_STEP):
        for volt in range(START_VOLT, 1301, VOLT_STEP):
            print(f"Testing {freq} MHz, {volt} mV...")
            status = test_settings(freq, volt)
            if status:
                results.append((freq, volt, status["hashrate"], status["asic_temp"], status["vr_temp"]))
                if status["hashrate"] > best_settings["hashrate"]:
                    best_settings = {"freq": freq, "volt": volt, "hashrate": status["hashrate"]}
            else:
                print("Reverting to safe...")
                set_miner_settings(725, 1150)
            time.sleep(60)  # Cooldown

    # Generate final 3D visualization
    if results:
        freqs, volts, hashrates, asic_temps, vr_temps = zip(*results)
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(freqs, volts, hashrates, c=vr_temps, cmap='hot', s=50)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('Voltage (mV)')
        ax.set_zlabel('Hashrate (TH/s)')
        ax.set_title('Hashrate vs Freq/Volt, Colored by VR Temp')
        fig.colorbar(scatter, ax=ax, label='VR Temp (°C)')
        expanded_path = os.path.expanduser(PLOT_PATH)
        plt.savefig(expanded_path)
        plt.close()
        print(f"Saved final plot: {expanded_path}")

    print(f"Best settings: {best_settings['freq']} MHz, {best_settings['volt']} mV, Hashrate {best_settings['hashrate']} TH/s")
    set_miner_settings(best_settings['freq'], best_settings['volt'])

if __name__ == "__main__":
    main()
