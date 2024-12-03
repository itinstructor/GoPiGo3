# Import necessary modules from evdev library
from evdev import InputDevice, categorize, ecodes

# Create an InputDevice instance to access the input event device
dev = InputDevice('/dev/input/event2')
# device /dev/input/event2, name "Wireless Controller", phys "aa:aa:aa:aa:aa:aa", uniq "58:10:31:3b:fd:b8"


# Print the details of the input device
print(dev)

# Loop to read events from the input device
for event in dev.read_loop():
    # Use categorize to interpret the event
    categorized_event = categorize(event)

    # Check if the event type is a key press event
    if event.type == ecodes.EV_KEY:

        # Print the categorized event details indicating a button press
        print(f"{categorized_event} button is pressed")
        print(f"{event} button is pressed")

    # Commented this out as the thumbwheels generate too much information
    # Check if the event type is an absolute axis event from thumb wheels
    # elif event.type == ecodes.EV_ABS:
    #     # Print the categorized event details for absolute axis events
    #     print(categorized_event)
    #     print(event)
