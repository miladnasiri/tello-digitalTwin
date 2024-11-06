# communication/commands.py

from enum import Enum
from typing import Dict, Optional, Tuple
import sys
sys.path.append('..')
from config.tello_specs import FLIGHT, VISION

class TelloCommands(Enum):
    """
    Actual Tello commands from manual
    """
    # Basic Control Commands
    COMMAND = "command"            # Enter SDK mode
    TAKEOFF = "takeoff"           # Auto takeoff
    LAND = "land"                 # Auto land
    EMERGENCY = "emergency"       # Emergency stop motors
    STOP = "stop"                # Stop moving and hover
    
    # Movement Commands
    UP = "up"                    # Move up x cm
    DOWN = "down"                # Move down x cm
    LEFT = "left"                # Move left x cm
    RIGHT = "right"              # Move right x cm
    FORWARD = "forward"          # Move forward x cm
    BACK = "back"                # Move backward x cm
    
    # Rotational Commands
    CW = "cw"                    # Rotate clockwise x degrees
    CCW = "ccw"                  # Rotate counter-clockwise x degrees
    
    # Speed Command
    SPEED = "speed"              # Set speed x cm/s
    
    # Read Commands
    BATTERY = "battery?"         # Get battery percentage
    SPEED_READ = "speed?"        # Get current speed
    TIME = "time?"              # Get flight time
    HEIGHT = "height?"          # Get height
    TEMP = "temp?"             # Get temperature
    ATTITUDE = "attitude?"     # Get IMU attitude data

class CommandHandler:
    """
    Handles Tello commands and validates parameters
    """
    def __init__(self, state_controller):
        self.state = state_controller
        self.command_limits = {
            'movement': {
                'min': 20,    # minimum 20cm movement
                'max': 500    # maximum 500cm movement
            },
            'rotation': {
                'min': 1,     # minimum 1 degree rotation
                'max': 360    # maximum 360 degree rotation
            },
            'speed': {
                'min': 10,    # minimum 10cm/s
                'max': 100    # maximum 100cm/s
            }
        }

    def execute_command(self, command: str, params: Optional[str] = None) -> Tuple[bool, str]:
        """
        Execute a Tello command with parameters
        Returns: (success, message)
        """
        try:
            cmd = TelloCommands(command)
            
            # Basic Commands
            if cmd == TelloCommands.TAKEOFF:
                success = self.state.take_off()
                return success, "Takeoff successful" if success else "Takeoff failed"
                
            elif cmd == TelloCommands.LAND:
                success = self.state.land()
                return success, "Landing successful" if success else "Landing failed"
                
            elif cmd == TelloCommands.EMERGENCY:
                self.state.emergency_stop()
                return True, "Emergency stop executed"
                
            # Movement Commands
            elif cmd in [TelloCommands.UP, TelloCommands.DOWN]:
                if not params:
                    return False, "Distance parameter required"
                distance = int(params)
                if not self._validate_movement(distance):
                    return False, f"Invalid distance: {distance}cm"
                
                current_height = self.state.height * 100  # convert to cm
                new_height = (current_height + distance if cmd == TelloCommands.UP 
                            else current_height - distance)
                success = self.state.set_height(new_height / 100)  # convert back to meters
                return success, f"Height adjusted to {new_height}cm"
                
            elif cmd in [TelloCommands.LEFT, TelloCommands.RIGHT, 
                        TelloCommands.FORWARD, TelloCommands.BACK]:
                if not params:
                    return False, "Distance parameter required"
                distance = int(params)
                if not self._validate_movement(distance):
                    return False, f"Invalid distance: {distance}cm"
                
                success = self.state.move(cmd.value, distance)
                return success, f"Moved {cmd.value} {distance}cm"
                
            # Rotation Commands
            elif cmd in [TelloCommands.CW, TelloCommands.CCW]:
                if not params:
                    return False, "Angle parameter required"
                angle = int(params)
                if not self._validate_rotation(angle):
                    return False, f"Invalid angle: {angle}degrees"
                
                success = self.state.rotate(cmd.value, angle)
                return success, f"Rotated {cmd.value} {angle}degrees"
                
            # Speed Command
            elif cmd == TelloCommands.SPEED:
                if not params:
                    return False, "Speed parameter required"
                speed = int(params)
                if not self._validate_speed(speed):
                    return False, f"Invalid speed: {speed}cm/s"
                
                success = self.state.set_speed(speed)
                return success, f"Speed set to {speed}cm/s"
                
            # Read Commands
            elif cmd == TelloCommands.BATTERY:
                return True, str(self.state.battery)
            elif cmd == TelloCommands.SPEED_READ:
                return True, str(self.state.speed)
            elif cmd == TelloCommands.HEIGHT:
                return True, str(int(self.state.height * 100))  # convert to cm
            elif cmd == TelloCommands.TEMP:
                return True, f"{self.state.temp_low}~{self.state.temp_high}°C"
                
            return False, f"Command {command} not implemented"
            
        except ValueError:
            return False, f"Invalid command: {command}"
        except Exception as e:
            return False, f"Error executing command: {str(e)}"
    
    def _validate_movement(self, distance: int) -> bool:
        """Validate movement distance"""
        return self.command_limits['movement']['min'] <= distance <= self.command_limits['movement']['max']
    
    def _validate_rotation(self, angle: int) -> bool:
        """Validate rotation angle"""
        return self.command_limits['rotation']['min'] <= angle <= self.command_limits['rotation']['max']
    
    def _validate_speed(self, speed: int) -> bool:
        """Validate speed value"""
        return self.command_limits['speed']['min'] <= speed <= self.command_limits['speed']['max']