
import importlib
import sys
from mock_data import states
importlib.reload(states)  # Force reload the module
from mock_data.states import TelloState

def test_drone():
    # Create drone instance
    tello = TelloState()
    
    def print_state(message):
        state = tello.get_state_dict()
        print(f"\n{message}:")
        for key, value in state.items():
            print(f"{key}: {value}")
        print("-" * 50)

    # Test sequence
    print_state("1. Initial State")
    
    print("\nTaking off...")
    success = tello.take_off()
    print(f"Takeoff {'successful' if success else 'failed'}")
    print_state("2. After Takeoff")
    
    print("\nChanging height to 1 meter...")
    success = tello.set_height(1.0)
    print(f"Height change {'successful' if success else 'failed'}")
    print_state("3. After Height Change")
    
    print("\nMoving forward 50cm...")
    success = tello.move('forward', 50)
    print(f"Movement {'successful' if success else 'failed'}")
    print_state("4. After Forward Movement")
    
    print("\nRotating 90 degrees clockwise...")
    success = tello.rotate('cw', 90)
    print(f"Rotation {'successful' if success else 'failed'}")
    print_state("5. After Rotation")
    
    print("\nLanding...")
    success = tello.land()
    print(f"Landing {'successful' if success else 'failed'}")
    print_state("6. Final State")

if __name__ == "__main__":
    print("Starting drone test...")
    test_drone()
