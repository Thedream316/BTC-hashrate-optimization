# BTC-hashrate-optimization
BTC hashrate optimization scripts for Bitaxe miner, including focused tuner for high-freq overclocks.
This repository, "BTC hashrate optimization," serves as a collection of Python scripts designed to automate and optimize the overclocking process for Bitaxe Bitcoin miners (specifically models like the Gamma with BM1370 ASIC chips). The primary goal is to maximize hashrate for solo mining while maintaining stability, monitoring temperatures (ASIC and voltage regulator), and ensuring safe operation through API interactions with the AxeOS firmware. These tools were developed through iterative testing, focusing on frequency (MHz) and voltage (mV) tuning to push performance beyond stock levels (e.g., from ~1.2 TH/s to 1.8-2.1 TH/s with custom cooling).
The scripts incorporate features like phased testing (quick scans followed by detailed averages), real-time status fetching, safety reverts on temperature thresholds, and visualizations for data analysis. They are built for users with basic Python setup on macOS (or similar), requiring libraries like requests and matplotlib. Always monitor your hardware to avoid damage—overclocking increases power draw (15-30W) and heat, and results vary by cooling mods (e.g., copper heatsinks and VR thermal pads).
Key Script: bitaxe_focused_tuner.py
This script (bitaxe_focused_tuner.py) is a specialized tuner for high-performance ranges, emphasizing frequencies from 800-900 MHz and voltages from 1250-1300 mV—ideal for pushing hashrate after initial broad tests. It runs 15-minute stability checks per combination, logs metrics (hashrate, ASIC/VR temps), and generates a 3D visualization at the end (hashrate vs freq/volt, colored by VR Temp) to identify correlations (e.g., VR heat throttling above 80°C).
Features:

API Integration: Uses Bitaxe's /api/system endpoint to set frequency/voltage and fetch status (/api/system/info).
Safety Mechanisms: Reverts to safe settings (725 MHz / 1150 mV) if ASIC temp exceeds 65°C; includes retries for network glitches.
Testing Loop: Iterates over specified ranges, with 60-second cooldowns to prevent overheating.
Visualization: Produces a 3D scatter plot saved as focused_run_plot.png, helping visualize optimal spots (e.g., high hashrate with low VR Temp).
Dependencies: requests for API calls, matplotlib and mpl_toolkits for plots, os for path handling. Install with pip install requests matplotlib.

Usage:

Edit config variables (e.g., IP, ranges, duration) as needed.
Run: python3 bitaxe_focused_tuner.py.
Monitor output and dashboard (http://192.168.1.19/).
At end, view the plot and apply best settings.

Example Output (from your run):

Best: 825 MHz / 1250 mV at ~1.838 TH/s (ASIC 61.875°C, VR 76°C).
Unstable higher combos highlight temp limits—VR cooling helped reduce VR Temps by ~5-10°C.

Limitations and Safety:

Risk of hardware damage if temps spike—use at own risk.
Network-dependent; ensure Bitaxe is connected.
For advanced users: Extend with VR temp thresholds or irregular freq tests (though not recommended due to PLL constraints).

Future Enhancements:

Add VR temp limits to stability.
Integrate reboot commands for settings application.
Support for multiple Bitaxes or cloud monitoring.

This repo can evolve into a full toolkit for miner optimization—feel free to contribute! For questions, open an issue.
