# utils/visualizer.py

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import threading
import time

class TelloVisualizer:
    def __init__(self):
        # Initialize the figure with subplots
        self.fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "scene", "rowspan": 2}, {"type": "indicator"}],
                  [None, {"type": "indicator"}]],
            subplot_titles=('Tello 3D Position', 'Battery Level', 'Height')
        )
        
        # Initialize drone position
        self.drone_position = {
            'x': [0], 'y': [0], 'z': [0],
            'history_x': [], 'history_y': [], 'history_z': []
        }
        
        # Setup 3D scene
        self._setup_3d_scene()
        
        # Setup indicators
        self._setup_indicators()
        
        # Update layout
        self.fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Tello Digital Twin Visualization",
        )
        
    def _setup_3d_scene(self):
        # Add drone marker
        self.fig.add_trace(
            go.Scatter3d(
                x=self.drone_position['x'],
                y=self.drone_position['y'],
                z=self.drone_position['z'],
                mode='markers+text',
                marker=dict(size=10, color='red'),
                text=['Tello'],
                name='Drone Position'
            ),
            row=1, col=1
        )
        
        # Add trajectory path
        self.fig.add_trace(
            go.Scatter3d(
                x=self.drone_position['history_x'],
                y=self.drone_position['history_y'],
                z=self.drone_position['history_z'],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Flight Path'
            ),
            row=1, col=1
        )
        
        # Update 3D scene layout
        self.fig.update_scenes(
            xaxis_range=[-2, 2],
            yaxis_range=[-2, 2],
            zaxis_range=[0, 3],
            aspectmode='cube'
        )
        
    def _setup_indicators(self):
        # Battery indicator
        self.fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Battery %"},
                gauge={'axis': {'range': [0, 100]},
                       'steps': [
                           {'range': [0, 20], 'color': "red"},
                           {'range': [20, 50], 'color': "yellow"},
                           {'range': [50, 100], 'color': "green"}]
                       }
            ),
            row=1, col=2
        )
        
        # Height indicator
        self.fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=0,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Height (m)"},
                gauge={'axis': {'range': [0, 10]},
                       'steps': [
                           {'range': [0, 1], 'color': "lightgray"},
                           {'range': [1, 5], 'color': "gray"},
                           {'range': [5, 10], 'color': "darkgray"}]
                       }
            ),
            row=2, col=2
        )

    def update_position(self, x, y, z, battery, yaw):
        # Update drone position
        self.drone_position['x'] = [x]
        self.drone_position['y'] = [y]
        self.drone_position['z'] = [z]
        
        # Update history
        self.drone_position['history_x'].append(x)
        self.drone_position['history_y'].append(y)
        self.drone_position['history_z'].append(z)
        
        # Update 3D position
        self.fig.update_traces(
            x=self.drone_position['x'],
            y=self.drone_position['y'],
            z=self.drone_position['z'],
            selector=dict(mode='markers+text')
        )
        
        # Update trajectory
        self.fig.update_traces(
            x=self.drone_position['history_x'],
            y=self.drone_position['history_y'],
            z=self.drone_position['history_z'],
            selector=dict(mode='lines')
        )
        
        # Update indicators
        self.fig.update_traces(
            value=battery,
            selector=dict(title={'text': "Battery %"})
        )
        
        self.fig.update_traces(
            value=z,
            selector=dict(title={'text': "Height (m)"})
        )

    def show(self):
        self.fig.show()