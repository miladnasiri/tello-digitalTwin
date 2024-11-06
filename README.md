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


Dashboard will be available at: http://localhost:8501
Dashboard Controls

Basic Flight: Takeoff, Land, Emergency Stop
Movement: Forward/Back, Left/Right
Height Control: 0.3m - 10.0m adjustment
Rotation: Clockwise/Counter-clockwise
Real-time State Display: Position, Battery, Temperature

Project Structure
Copytello-simulation/
├── config/           # Drone specifications
├── mock_data/        # State simulation
├── tests/            # Dashboard implementation  
└── utils/           # Visualization tools
Technical Details

Height Range: 0.3m - 10.0m
Max Speed: 28.8 km/h
Vision System Range: 0.3-10m
Battery Simulation: Realistic drain
Temperature Range: 0°C - 40°C

Contributing
Pull requests welcome! Please read CONTRIBUTING.md first.
License
MIT
Contact
Milad Nasiri - GitHub Profile
EOL
