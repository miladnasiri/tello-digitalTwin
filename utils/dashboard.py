# utils/dashboard.py

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time
import threading
from queue import Queue

class TelloDashboard:
    def __init__(self, tello_state):
        self.tello = tello_state
        self.command_queue = Queue()
        self.setup_dashboard()
        
    def setup_dashboard(self):
        st.title("Tello Digital Twin Dashboard")
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Digital Twin Control")
            self.setup_command_interface()
            self.setup_state_display()
            
        with col2:
            st.header("Physical Drone Interface")
            self.setup_real_drone_interface()
            
    def setup_command_interface(self):
        st.subheader("Command Center")
        
        # Basic Commands
        basic_cmd = st.selectbox(
            "Basic Commands",
            ["takeoff", "land", "emergency", "stop"]
        )
        if st.button("Execute Basic Command"):
            self.command_queue.put(basic_cmd)
            
        # Movement Commands
        st.subheader("Movement Control")
        col1, col2 = st.columns(2)
        
        with col1:
            direction = st.selectbox(
                "Direction",
                ["up", "down", "left", "right", "forward", "back"]
            )
            
        with col2:
            distance = st.number_input(
                "Distance (cm)",
                min_value=20,
                max_value=500,
                value=100
            )
            
        if st.button("Execute Movement"):
            cmd = f"{direction} {distance}"
            self.command_queue.put(cmd)
            
        # Rotation Control
        st.subheader("Rotation Control")
        rot_dir = st.selectbox("Rotation", ["cw", "ccw"])
        angle = st.number_input(
            "Angle (degrees)",
            min_value=1,
            max_value=360,
            value=90
        )
        
        if st.button("Execute Rotation"):
            cmd = f"{rot_dir} {angle}"
            self.command_queue.put(cmd)
            
    def setup_state_display(self):
        st.subheader("Digital Twin State")
        
        # Create metrics display
        col1, col2, col3 = st.columns(3)
        
        state = self.tello.get_state_dict()
        
        with col1:
            st.metric("Height (m)", f"{state['height']:.2f}")
            st.metric("Battery %", state['battery'])
            
        with col2:
            st.metric("Speed (km/h)", f"{state['speed']:.1f}")
            st.metric("Flight Time (s)", state['flight_time'])
            
        with col3:
            st.metric("Temperature °C", 
                     f"{state['temp_low']}~{state['temp_high']}")
            st.metric("Vision System", 
                     "Active" if state['vision_system'] else "Inactive")
            
    def setup_real_drone_interface(self):
        st.subheader("Real Drone Connection")
        
        # Connection status
        status = st.empty()
        status.info("Waiting for drone connection...")
        
        # IP and Port configuration
        ip = st.text_input("Drone IP", "192.168.10.1")
        port = st.number_input("Port", value=8889)
        
        if st.button("Connect to Real Drone"):
            status.success("Connected to drone!")
            
        # Command response area
        st.subheader("Command Response")
        response_area = st.empty()
        response_area.code("Waiting for commands...")
        
    def update_visualization(self):
        # Create 3D visualization
        fig = go.Figure(data=[
            go.Scatter3d(
                x=[self.tello.x_pos],
                y=[self.tello.y_pos],
                z=[self.tello.height],
                mode='markers+text',
                marker=dict(size=10, color='red'),
                text=['Drone'],
                name='Current Position'
            )
        ])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='X Position (m)',
                yaxis_title='Y Position (m)',
                zaxis_title='Height (m)',
                aspectmode='cube'
            ),
            title='Drone Position'
        )
        
        st.plotly_chart(fig)
        
    def process_commands(self):
        while True:
            if not self.command_queue.empty():
                cmd = self.command_queue.get()
                # Process command for both digital twin and real drone
                # This is where we'll add the bidirectional communication
                self.execute_command(cmd)
            time.sleep(0.1)
            
    def execute_command(self, cmd):
        # Execute on digital twin
        response = self.tello.execute_command(cmd)
        
        # If connected to real drone, execute there too
        # This is where we'll add the real drone communication
        
        return response