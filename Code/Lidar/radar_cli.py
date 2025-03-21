# Import required libraries
from easygopigo3 import EasyGoPiGo3  # Import the GoPiGo3 robot control library
import time  # Import time library for adding delays
import math  # Import math library for trigonometric calculations
LEFT = 20
RIGHT = 160
CENTER = 85


class DistanceScanner:
    # This class handles all the scanning functionality for the GoPiGo3 robot
    def __init__(self):
        # This is the constructor method - it runs when we create a new DistanceScanner object

        # Create a GoPiGo3 object to control the robot
        self.gpg = EasyGoPiGo3()

        # Initialize the distance sensor on port AD1
        # The distance sensor measures how far away objects are
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")

        # Initialize the servo motor on port SERVO2
        # The servo motor will rotate the distance sensor to different angles
        self.servo2 = self.gpg.init_servo("SERVO2")

        # Set up scanning parameters
        # range(20, 160, 20) creates a sequence: 20, 40, 60, 80, 100, 120, 140
        # These are the angles (in degrees) where the servo will take measurements
        self.scan_range = range(LEFT, RIGHT, LEFT)

        # Time to wait after moving servo (in seconds)
        # This gives the servo time to reach its position
        self.servo_delay = 0.1

        # Create an empty list to store scan results
        self.scan_results = []

# --------------------------- MOVE SERVO --------------------------------- #
    def move_servo(self, angle):
        """Move servo to specified angle and wait for it to reach position"""
        # Tell the servo motor to move to the specified angle
        self.servo2.rotate_servo(angle)
        # Wait for the servo to reach its position
        time.sleep(self.servo_delay)

# --------------------------TAKE MEASUREMENT ----------------------------- #
    def take_measurement(self):
        """Take a distance measurement and return it in centimeters"""
        # Read distance in millimeters and convert to centimeters by dividing by 10
        return self.distance_sensor.read_mm() / 10

# ------------------------ PERFORM SCAN ---------------------------------- #
    def perform_scan(self):
        """Perform a full scan and store results"""
        # Clear any previous scan results
        self.scan_results = []

        print("Starting scan...")
        # For each angle in our scan range
        for angle in self.scan_range:
            # Move the servo to the current angle
            self.move_servo(angle)

            # Take a distance measurement
            distance = self.take_measurement()

            # Store the angle and distance in our results list
            # Each result is stored as a dictionary with 'angle' and 'distance' keys
            self.scan_results.append({
                'angle': angle,
                'distance': distance
            })

            # Print the current measurement
            print(f"Angle: {angle}°, Distance: {distance:.1f}cm")

        # After scanning, return servo to center position (90 degrees)
        self.move_servo(90)

# ------------------ PRINT _ ASCII VISUALIZATION ------------------------- #
    def print_ascii_visualization(self):
        """Create a simple ASCII visualization of the scan results"""
        # Print explanation of the visualization
        print("\nScan Visualization (top-down view):")
        print("Robot is at 'R', * represents detected objects")
        print("Each character represents approximately 20cm\n")

        # Create a 2D grid for our visualization
        width = 41  # Must be odd to have a center point
        height = 21
        # Create empty grid filled with spaces
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Calculate center position for robot
        center_x = width // 2  # Center horizontally
        center_y = height - 1  # Bottom row
        # Place robot marker 'R' at center bottom
        grid[center_y][center_x] = 'R'

        # Set scale factor (20cm per character to show up to 400cm)
        scale = 0.05  # 1/20 = 0.05 (each grid unit represents 20cm)

        # Plot each scan point on the grid
        for point in self.scan_results:
            # Convert angle to radians and adjust so 90° is forward
            angle_rad = math.radians(point['angle'] - 90)

            # Convert real-world distance to grid units
            distance = point['distance'] * scale

            # Only plot points with valid distances (greater than 0)
            if distance > 0:
                # Calculate grid coordinates using trigonometry
                x = int(center_x + (distance * math.cos(angle_rad)))
                y = int(center_y - (distance * math.sin(angle_rad)))

                # If calculated position is within grid bounds
                if 0 <= x < width and 0 <= y < height:
                    # Place an asterisk '*' to mark detected object
                    grid[y][x] = '*'

        # Create distance markers (100cm, 200cm, 300cm, 400cm)
        # Convert real distances to grid units
        markers = [100, 200, 300, 400]  # distances in cm
        for distance in markers:
            grid_dist = int(distance * scale)
            if grid_dist < height:
                grid[height - 1 - grid_dist][center_x] = '+'  # Forward marker

        # Create border for visualization
        border = '+' + '-' * (width) + '+'
        print(border)

        # Print each row of the grid with side borders
        for i, row in enumerate(grid):
            # Add distance labels on the right side for marker rows
            distance_label = ""
            for marker in markers:
                if height - 1 - i == int(marker * scale):
                    distance_label = f" {marker}cm"
                    break
            print('|' + ''.join(row) + '|' + distance_label)

        print(border)
        print("\nScale: Each character represents approximately 20cm")
        print("Maximum visualization range: ~400cm")
        print("'+' marks show 100cm, 200cm, 300cm, and 400cm distances")

# ------------------------ RESET GOPIGO ---------------------------------- #
    def reset(self):
        self.servo2.disable_servo()
        self.gpg.reset_all()


def main():
    # Create a new DistanceScanner object
    scanner = DistanceScanner()

    try:
        # Main program loop
        while True:
            # Wait for user to press Enter
            input("Press Enter to perform a scan (Ctrl+C to exit)...")
            # Perform scan and get results
            scanner.perform_scan()
            # Show visualization of results
            scanner.print_ascii_visualization()

    except KeyboardInterrupt:
        # If user presses Ctrl+C, exit gracefully
        print("\nScanning terminated by user")
        # Return servo to center position before exiting
        scanner.move_servo(90)
        scanner.reset()


if __name__ == "__main__":
    main()
