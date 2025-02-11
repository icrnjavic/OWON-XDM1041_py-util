import tkinter as tk
from tkinter import ttk
import time

class OwonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Owon Digital Multimeter")
        self.root.geometry("800x650")
        
        style = ttk.Style()
        style.configure("Digital.TLabel", font=("Digital-7", 48), background="black", foreground="#00ff00")
        style.configure("Unit.TLabel", font=("Digital-7", 24), background="black", foreground="#00ff00")
        style.configure("Mode.TButton", padding=5)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.display_frame = ttk.Frame(self.main_frame, style="Digital.TFrame")
        self.display_frame.pack(fill=tk.X, pady=(0, 10))
        self.display_panel = ttk.Frame(self.display_frame)
        self.display_panel.pack(fill=tk.X, pady=10)
        self.display_panel.configure(style="Digital.TFrame")
        self.display_panel.tk_setPalette(background='black')
        self.reading_value = ttk.Label(self.display_panel, text="0.000", style="Digital.TLabel")
        self.reading_value.pack(pady=10)
        self.reading_unit = ttk.Label(self.display_panel, text="V DC", style="Unit.TLabel")
        self.reading_unit.pack()
        self.mode_frame = ttk.LabelFrame(self.main_frame, text="Measurement Mode")
        self.mode_frame.pack(fill=tk.X, pady=(0, 10))
        self.mode_buttons_frame = ttk.Frame(self.mode_frame)
        self.mode_buttons_frame.pack(pady=5)

        self.current_mode = tk.StringVar(value="voltage_dc")
        
        modes = [
            ("DC Voltage", "voltage_dc", "V Auto"),
            ("DC Current", "current_dc", "A Auto"),
            ("Resistance", "resistance", "Ω"),
        ]

        for text, mode, unit in modes:
            btn = ttk.Button(
                self.mode_buttons_frame,
                text=text,
                style="Mode.TButton",
                command=lambda m=mode, u=unit: self.change_mode(m, u)
            )
            btn.pack(side=tk.LEFT, padx=5)
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Measurement Log")
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_display = tk.Text(self.log_frame, height=10, width=40)
        self.log_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controls")
        self.control_frame.pack(fill=tk.X, pady=(10, 0))
        self.left_controls = ttk.Frame(self.control_frame)
        self.left_controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.right_controls = ttk.Frame(self.control_frame)
        self.right_controls.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(self.left_controls, text="Sample Rate (ms):").pack()
        self.sample_rate = ttk.Entry(self.left_controls)
        self.sample_rate.insert(0, "1000")
        self.sample_rate.pack(pady=(0, 10))
        ttk.Label(self.left_controls, text="Port:").pack()
        self.port_combo = ttk.Combobox(self.left_controls, values=["COM1", "COM2", "COM3", "COM4"])
        self.port_combo.pack(pady=(0, 10))
        self.start_button = ttk.Button(self.right_controls, text="Start", command=self.start_measurement)
        self.start_button.pack(fill=tk.X, pady=5)
        self.stop_button = ttk.Button(self.right_controls, text="Stop", command=self.stop_measurement)
        self.stop_button.pack(fill=tk.X, pady=5)
        self.is_running = False
        self.current_unit = "V DC"
        self.multimeter = None

    def change_mode(self, mode, unit):
        self.current_mode = mode
        self.current_unit = unit
        self.reading_unit.configure(text=unit)
        if self.is_running:
            self.stop_measurement()
            self.start_measurement()

    def start_measurement(self):
        try:
            if not self.multimeter:
                from OWON_XDM1042 import OWON_XDM1042
                port = self.port_combo.get()
                self.multimeter = OWON_XDM1042(port)
                
            self.is_running = True
            self.update_display()
            self.log_display.insert(tk.END, "Connected to OWON XDM1042\n")
            self.log_display.see(tk.END)
            
        except Exception as e:
            self.log_display.insert(tk.END, f"Error connecting to device: {str(e)}\n")
            self.log_display.see(tk.END)
            self.is_running = False

    def stop_measurement(self):
        """Stop measurements and close device connection."""
        self.is_running = False
        if self.multimeter:
            try:
                self.multimeter.close()
                self.multimeter = None
                self.log_display.insert(tk.END, "Disconnected from device\n")
                self.log_display.see(tk.END)
            except Exception as e:
                self.log_display.insert(tk.END, f"Error disconnecting: {str(e)}\n")
                self.log_display.see(tk.END)

    def update_display(self):
        if self.is_running and self.multimeter:
            try:
                # Get reading based on current mode
                reading = None
                if self.current_mode == "voltage_dc":
                    reading = self.multimeter.measure_voltage_dc()
                elif self.current_mode == "current_dc":
                    reading = self.multimeter.measure_current_dc()
                elif self.current_mode == "resistance":
                    reading = self.multimeter.measure_resistance()
                
                if reading is not None:
                    self.reading_value.configure(text=f"{reading:.3f}")
                    
                    # Update log with current reading
                    current_time = time.strftime("%H:%M:%S")
                    self.log_display.insert(tk.END, f"{current_time}: {reading:.3f} {self.current_unit}\n")
                    self.log_display.see(tk.END)
                
            except Exception as e:
                self.log_display.insert(tk.END, f"Error reading from device: {str(e)}\n")
                self.log_display.see(tk.END)
                self.is_running = False
                return
                
            self.root.after(int(self.sample_rate.get()), self.update_display)

if __name__ == "__main__":
    root = tk.Tk()
    app = OwonGUI(root)
    root.mainloop()