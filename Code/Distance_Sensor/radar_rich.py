from easygopigo3 import EasyGoPiGo3
from time import sleep
from math import cos, sin, radians
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout


class DistanceScanner:
    def __init__(self):
        self.gpg = EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor("AD1")
        self.servo2 = self.gpg.init_servo("SERVO2")
        self.scan_range = range(20, 160, 20)
        self.servo_delay = 0.1
        self.scan_results = []
        self.console = Console()

    def move_servo(self, angle):
        """Move servo to specified angle and wait for it to reach position"""
        self.servo2.rotate_servo(angle)
        sleep(self.servo_delay)

    def take_measurement(self):
        """Take a distance measurement and return it in centimeters"""
        return self.distance_sensor.read_mm() / 10

    def perform_scan(self):
        """Perform a full scan and store results"""
        self.scan_results = []

        self.console.print("[bold blue]Starting scan...[/bold blue]")
        for angle in self.scan_range:
            self.move_servo(angle)
            distance = self.take_measurement()
            self.scan_results.append({
                'angle': angle,
                'distance': distance
            })
            msg = f"[green]Angle:[/green] [yellow]{angle}°[/yellow], "
            msg += f"[green]Distance:[/green]"
            msg += f"[yellow]{distance:.1f}cm[/yellow]"
            self.console.print(msg)

        self.move_servo(90)
        return self.scan_results

    def print_ascii_visualization(self):
        """Create a rich ASCII visualization of the scan results"""
        # Create layout for visualization
        layout = Layout()

        # Initialize visualization components
        width = 41  # Must be odd to have a center point
        height = 21
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Calculate center position
        center_x = width // 2
        center_y = height - 1
        grid[center_y][center_x] = 'R'

        # Set scale factor (20cm per character)
        scale = 0.05

        # Plot scan points
        for point in self.scan_results:
            angle_rad = radians(point['angle'] - 90)
            distance = point['distance'] * scale

            if distance > 0:
                x = int(center_x + (distance * cos(angle_rad)))
                y = int(center_y - (distance * sin(angle_rad)))

                if 0 <= x < width and 0 <= y < height:
                    grid[y][x] = '*'

        # Add distance markers
        markers = [100, 200, 300, 400]
        for distance in markers:
            grid_dist = int(distance * scale)
            if grid_dist < height:
                grid[height - 1 - grid_dist][center_x] = '+'

        # Create visualization text
        viz_text = Text()

        # Add border and grid content with colored elements
        border = '+' + '-' * width + '+'
        viz_text.append(border + '\n', style="bright_blue")

        for i, row in enumerate(grid):
            line = Text()
            line.append('|', style="bright_blue")

            for char in row:
                if char == 'R':
                    line.append(char, style="bold red")
                elif char == '*':
                    line.append(char, style="bold yellow")
                elif char == '+':
                    line.append(char, style="bright_green")
                else:
                    line.append(char)

            line.append('|', style="bright_blue")

            # Add distance labels
            for marker in markers:
                if height - 1 - i == int(marker * scale):
                    line.append(f" {marker}cm", style="bright_cyan")

            viz_text.append(line)
            viz_text.append('\n')

        viz_text.append(border, style="bright_blue")

        # Create legend
        legend = Text()
        legend.append("\nLegend:\n", style="bold")
        legend.append("R ", style="bold red")
        legend.append("- Robot Position\n")
        legend.append("* ", style="bold yellow")
        legend.append("- Detected Objects\n")
        legend.append("+ ", style="bright_green")
        legend.append("- Distance Markers (100cm, 200cm, 300cm, 400cm)\n")
        legend.append(
            "\nScale: Each character represents approximately 20cm\n")
        legend.append("Maximum visualization range: ~400cm")

        # Create panel with visualization and legend
        panel = Panel(
            viz_text + legend,
            title="[bold]Scan Visualization (top-down view)[/bold]",
            border_style="bright_blue"
        )

        # Print the final visualization
        self.console.print(panel)

    def reset(self):
        self.servo2.disable_servo()
        self.gpg.reset_all()


def main():
    scanner = DistanceScanner()
    console = Console()

    try:
        while True:
            console.print(
                "\n[bold cyan]Press Enter to perform a scan (Ctrl+C to exit)...[/bold cyan]")
            input()
            results = scanner.perform_scan()
            scanner.print_ascii_visualization()

    except KeyboardInterrupt:
        console.print("\n[bold red]Scanning terminated by user[/bold red]")
        scanner.move_servo(90)
        scanner.reset()


if __name__ == "__main__":
    main()
