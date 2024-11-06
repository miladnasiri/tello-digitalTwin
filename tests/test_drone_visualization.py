# tests/test_drone_visualization.py

import sys
import time
import importlib
sys.path.append('..')
from mock_data.states import TelloState
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, clear_output

class DroneVisualizer:
    def __init__(self):
        self.fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "scene", "rowspan": 2}, {"type": "indicator"}],
                  [None, {"type": "indicator"}]],
            subplot_titles=('Drone Position', 'Battery', 'Height')
        )
        self._setup_plot()
        
    def _setup_plot(self):
        # 3D Scene
        self.fig.add_trace(
            go.Scatter3d(
                x=[0], y=[0], z=[0],
                mode='markers+text',
                marker=dict(size=10, color='red'),
                text=['Drone'],
                name='Position'
            ),
            row=1, col=1
        )
        
        # Battery Indicator
        self.fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=100,
                title={'text': "Battery %"},
                gauge={'axis': {'range': [0, 100]}},
            ),
            row=1, col=2
        )
        
        # Height Indicator
        self.fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=0,
                title={'text': "Height (m)"},
                gauge={'axis': {'range': [0, 10]}},
            ),
            row=2, col=2
        )
        
        self.fig.update_layout(height=800, showlegend=False)
        
    def update(self, state):
        with self.fig.batch_update():
            # Update position
            self.fig.data[0].x = [state['x_pos']]
            self.fig.data[0].y = [state['y_pos']]
            self.fig.data[0].z = [state['height']]
            
            # Update indicators
            self.fig.data[1].value = state['battery']
            self.fig.data[2].value = state['height']
        
        clear_output(wait=True)
        display(self.fig)

def test_drone_with_visualization():
    # Initialize drone and visualizer
    tello = TelloState()
    viz = DroneVisualizer()
    
    # Test sequence
    print("Starting test sequence...")
    
    # Initial state
    viz.update(tello.get_state_dict())
    time.sleep(2)
    
    # Takeoff
    print("Taking off...")
    tello.take_off()
    viz.update(tello.get_state_dict())
    time.sleep(2)
    
    # Move up
    print("Moving up...")
    tello.set_height(1.0)
    viz.update(tello.get_state_dict())
    time.sleep(2)
    
    # Move forward
    print("Moving forward...")
    tello.move('forward', 100)
    viz.update(tello.get_state_dict())
    time.sleep(2)
    
    # Land
    print("Landing...")
    tello.land()
    viz.update(tello.get_state_dict())

if __name__ == "__main__":
    test_drone_with_visualization()