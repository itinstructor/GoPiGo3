# Import necessary modules from evdev library
from evdev import InputDevice, categorize, ecodes, KeyEvent

# Function to find and return the connected game controller
def find_controller():
    gamepad = None
    try:
        # List of potential event device paths
        event_devices = ['/dev/input/event0', '/dev/input/event1', '/dev/input/event2', '/dev/input/event3']
        
        # List of supported game controllers
        controller_list = [
            "Logitech Gamepad F710",
            "Logitech Gamepad F310",
            "Microsoft X-Box 360 pad"
        ]

        # Loop through each event device path
        for event_path in event_devices:
            # Create InputDevice instance for the current event device path
            device = InputDevice(event_path)
            
            # Check if the device name matches any controller in the list
            if device.name in controller_list:
                gamepad = device
                print(gamepad)
                break
        
        # If no match is found, print a message
        if gamepad is None:
            print("controller not found")
            
    except Exception as e:
        pass
        print(f"Error: {e}")

    
    # Return the identified gamepad
    return gamepad

# Call the find_controller function and store the result in the gamepad variable
gamepad = find_controller()
print(gamepad)
