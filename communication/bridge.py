# communication/bridge.py

import socket
import threading
import time
from queue import Queue

class TelloBridge:
    def __init__(self, simulator):
        self.simulator = simulator
        self.real_drone = None
        self.command_queue = Queue()
        self.response_queue = Queue()
        
    def connect_real_drone(self, ip="192.168.10.1", port=8889):
        """Connect to real Tello drone"""
        try:
            self.real_drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.real_drone.bind(('', 8890))
            self.real_drone.sendto(b'command', (ip, port))
            response = self.real_drone.recvfrom(1024)[0]
            return response.decode('utf-8') == 'ok'
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def send_command(self, command):
        """Send command to both simulator and real drone"""
        # Execute in simulator
        sim_response = self.simulator.execute_command(command)
        
        # If real drone connected, send command
        real_response = None
        if self.real_drone:
            try:
                self.real_drone.sendto(command.encode(), ('192.168.10.1', 8889))
                real_response = self.real_drone.recvfrom(1024)[0].decode()
            except Exception as e:
                real_response = f"Error: {e}"
                
        return {
            'simulator': sim_response,
            'real_drone': real_response
        }
        
    def start_state_monitoring(self):
        """Start monitoring state changes in both simulator and real drone"""
        def monitor_loop():
            while True:
                # Get simulator state
                sim_state = self.simulator.get_state_dict()
                
                # If real drone connected, get its state
                if self.real_drone:
                    try:
                        self.real_drone.sendto(b'state?', ('192.168.10.1', 8889))
                        real_state = self.real_drone.recvfrom(1024)[0].decode()
                    except:
                        real_state = None
                        
                # Compare and synchronize states
                self.synchronize_states(sim_state, real_state)
                
                time.sleep(0.1)
                
        threading.Thread(target=monitor_loop, daemon=True).start()
        
    def synchronize_states(self, sim_state, real_state):
        """Synchronize states between simulator and real drone"""
        if real_state:
            # Parse real drone state and update simulator
            # This ensures digital twin matches physical drone
            pass