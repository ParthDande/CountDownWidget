import tkinter as tk
from tkinter import colorchooser
from datetime import datetime
import json
import os
from pathlib import Path

class CountdownWidget:
    def __init__(self):
        # Create config directory if it doesn't exist
        self.config_dir = Path.home() / '.countdown_widget'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            'title': 'GATE Exam 2025',  # Updated title to include year
            'target_date': '2025-02-07 00:00:00',  # Corrected year to 2025
            'position_x': 100,
            'position_y': 100,
            'bg_color': 'black',
            'title_color': '#FFD700',  # Gold color for title
            'time_color': 'white'
        }
        
        # Load or create configuration
        self.load_config()
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Countdown Widget")
        
        # Make it stay on desktop level (below other windows)
        self.root.wm_attributes('-topmost', False)
        self.root.lower()  # Place window at the bottom of window stack
        self.root.overrideredirect(True)
        
        # Create the main frame
        self.frame = tk.Frame(
            self.root,
            bg=self.config['bg_color'],
            padx=10,
            pady=5
        )
        self.frame.pack(expand=True, fill='both')
        
        # Create labels
        self.title_label = tk.Label(
            self.frame,
            text=self.config['title'],
            font=('Arial', 12, 'bold'),
            bg=self.config['bg_color'],
            fg=self.config['title_color']
        )
        self.title_label.pack()
        
        self.time_label = tk.Label(
            self.frame,
            text="",
            font=('Arial', 20),
            bg=self.config['bg_color'],
            fg=self.config['time_color']
        )
        self.time_label.pack()
        
        # Add drag functionality
        self.frame.bind('<Button-1>', self.start_drag)
        self.frame.bind('<B1-Motion>', self.drag)
        
        # Add right-click menu
        self.create_context_menu()
        
        # Position the widget
        self.root.geometry(f"+{self.config['position_x']}+{self.config['position_y']}")
        
        # Start the countdown
        self.update_countdown()

    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                # Force update the title and target date
                self.config['title'] = self.default_config['title']
                self.config['target_date'] = self.default_config['target_date']
                # Update with any missing default values
                for key, value in self.default_config.items():
                    if key not in self.config:
                        self.config[key] = value
        else:
            self.config = self.default_config.copy()
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        # Save new position
        self.config['position_x'] = x
        self.config['position_y'] = y
        self.save_config()

    def create_context_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Change Background Color", command=self.choose_bg_color)
        self.menu.add_command(label="Change Title Color", command=self.choose_title_color)
        self.menu.add_command(label="Change Time Color", command=self.choose_time_color)
        self.menu.add_separator()
        self.menu.add_command(label="Send to Back", command=self.send_to_back)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.root.quit)
        self.frame.bind('<Button-3>', self.show_menu)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color", color=self.config['bg_color'])
        if color[1]:  # If a color was chosen (not cancelled)
            self.config['bg_color'] = color[1]
            self.frame.configure(bg=color[1])
            self.title_label.configure(bg=color[1])
            self.time_label.configure(bg=color[1])
            self.save_config()

    def choose_title_color(self):
        color = colorchooser.askcolor(title="Choose Title Color", color=self.config['title_color'])
        if color[1]:
            self.config['title_color'] = color[1]
            self.title_label.configure(fg=color[1])
            self.save_config()

    def choose_time_color(self):
        color = colorchooser.askcolor(title="Choose Time Color", color=self.config['time_color'])
        if color[1]:
            self.config['time_color'] = color[1]
            self.time_label.configure(fg=color[1])
            self.save_config()

    def send_to_back(self):
        self.root.lower()

    def update_countdown(self):
        try:
            target = datetime.strptime(self.config['target_date'], '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            
            if now > target:
                self.time_label.config(text="Best of luck!")
            else:
                delta = target - now
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                time_str = f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"
                self.time_label.config(text=time_str)
            
            # Update every second
            self.root.after(1000, self.update_countdown)
        except Exception as e:
            self.time_label.config(text="Error: Check date format")

if __name__ == "__main__":
    widget = CountdownWidget()
    widget.root.mainloop()