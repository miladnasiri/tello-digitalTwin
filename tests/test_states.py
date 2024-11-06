# tests/test_states.py

from mock_data.states import TelloState
import time

def test_drone_movements():
    # Initialize drone
    tello = TelloState()
    
    # Test sequence
    def print_state(message):
        print(f"\n{message}:")
        state = tello.get_state_dict()
        for key, value in state.items():
            print(f"{key}: {value}")
        print("-" * 50)

    # Initial state
    print_state("Initial State")
    
    # Takeoff
    tello.take_off()
    print_state("After Takeoff")
    
    # Move up
    tello.set_height(1.0)
    print_state("After Moving Up to 1m")
    
    # Move forward
    tello.move('forward', 50)
    print_state("After Moving Forward 50cm")
    
    # Rotate
    tello.rotate('cw', 90)
    print_state("After Rotating 90 degrees")
    
    # Move right
    tello.move('right', 30)
    print_state("After Moving Right 30cm")
    
    # Land
    tello.land()
    print_state("After Landing")

if __name__ == "__main__":
    test_drone_movements()