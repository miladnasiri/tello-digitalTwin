# Tello Drone Digital Twin Simulator

cat > README.md << 'EOL'
# Tello Drone Digital Twin Simulator

A digital twin simulation system for the DJI Tello drone that enables testing and visualization before using real hardware. Based on official Tello specifications for accurate simulation.

## Features
- Real-time state simulation (flight dynamics, battery, temperature)
- Interactive 3D visualization dashboard
- Flight controls simulation (takeoff, land, movement, rotation)
- Position and orientation tracking

## Quick Start

```bash
# Clone repository
git clone https://github.com/miladnasiri/tello-digitalTwin.git
cd tello-digitalTwin

# Install dependencies 
pip install -r requirements.txt

# Launch dashboard
streamlit run tests/test_dashboard.py
