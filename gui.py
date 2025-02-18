import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import time
from OWON_XDM1041 import OWONXDM1041


def get_instrument_id(multimeter):
    instrument_id = multimeter.query_instrument_id()
    return instrument_id


def configure_dc_voltage(multimeter):
    multimeter.configure_dc_voltage()
    time.sleep(3)


def configure_resistance(multimeter):
    multimeter.configure_resistance()
    time.sleep(3)


def measure_value(multimeter):
    measured_value = multimeter.measure_value()
    return measured_value


def open_serial_port(multimeter):
    result = multimeter.open_serial_port()
    return result


def close_serial_port(multimeter):
    result = multimeter.close_serial_port()
    return result


class OwonGUI:
    def switch_to_dc_voltage(self):
        if self.is_connected and self.multimeter:
            if self.update_id:
                self.root.after_cancel(self.update_id)
                self.update_id = None
            
            configure_dc_voltage(self.multimeter)
            self.start_continuous_measurement()

    def switch_to_resistance(self):
        if self.is_connected and self.multimeter:
            if self.update_id:
                self.root.after_cancel(self.update_id)
                self.update_id = None
            
            configure_resistance(self.multimeter)
            
            self.start_continuous_measurement()

    def start_continuous_measurement(self):
        """Update the measurement display continuously."""
        if self.is_connected and self.multimeter:
            try:
                print("Attempting to measure value...")
                value = measure_value(self.multimeter)
                print(f"Received value: {value}")
                self.value_display.configure(text=value)
            except Exception as e:
                print(f"Measurement error: {e}")
                
            self.update_id = self.root.after(100, self.start_continuous_measurement) # 100ms measurement interval
        else:
            print("Not connected or no multimeter instance")

    def __init__(self, root):
        self.root = root
        self.root.title("ODM GUI") # ODM - owon digital multimeter
        self.root.geometry("600x400")
        
        # Configure styles
        style = ttk.Style()
        style.configure('MainFrame.TFrame', background='#2c3e50')
        style.configure('Display.TFrame', background='#34495e')
        style.configure('Title.TLabel', 
                       background='#2c3e50',
                       foreground='white',
                       font=('Helvetica', 24, 'bold'))
        style.configure('Value.TLabel',
                       background='#34495e',
                       foreground='#2ecc71',
                       font=('Digital-7', 72))
        style.configure('Text.TLabel',
                       background='#2c3e50',
                       foreground='white',
                       font=('Helvetica', 12))
        
        style.configure('Connect.TButton',
                       padding=(20, 10),
                       font=('Helvetica', 12, 'bold'),
                       background='#e74c3c',
                       foreground='white')
        
        style.configure('Mode.TButton',
                       padding=(20, 10),
                       font=('Helvetica', 12),
                       background='#3498db',
                       foreground='white')
        
        style.map('Connect.TButton',
                 background=[('active', '#c0392b')],
                 foreground=[('active', 'white')])
        
        style.map('Mode.TButton',
                 background=[('active', '#2980b9')], 
                 foreground=[('active', 'white')])
        
        self.main_frame = ttk.Frame(self.root, style='MainFrame.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(self.main_frame, 
                              text="OWON XDM1041",
                              style='Title.TLabel')
        title_label.pack(pady=(20, 30))
        
        display_frame = ttk.Frame(self.main_frame, style='Display.TFrame', padding=20)
        display_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        self.value_display = ttk.Label(display_frame,
                                     text="0.000",
                                     style='Value.TLabel')
        self.value_display.pack(pady=10)
        
        port_frame = ttk.Frame(self.main_frame, style='MainFrame.TFrame')
        port_frame.pack(fill=tk.X, padx=40, pady=10)
        
        ttk.Label(port_frame,
                 text="Port:",
                 style='Text.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.port_combo = ttk.Combobox(port_frame,
                                      values=self.get_available_ports(),
                                      width=30,
                                      font=('Helvetica', 12))
        self.port_combo.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        control_frame = ttk.Frame(self.main_frame, style='MainFrame.TFrame')
        control_frame.pack(fill=tk.X, padx=40, pady=20)
        
        self.connect_button = ttk.Button(control_frame,
                                       text="Connect",
                                       command=self.toggle_connection,
                                       style='Connect.TButton')
        self.connect_button.pack(side=tk.LEFT, padx=6)
        
        # Mode buttons (hidden by default)
        self.dc_voltage_button = ttk.Button(control_frame,
                                          text="DC Voltage",
                                          command=self.switch_to_dc_voltage,
                                          style='Mode.TButton')
        
        self.resistance_button = ttk.Button(control_frame,
                                          text="Resistance",
                                          command=self.switch_to_resistance,
                                          style='Mode.TButton')
        
        self.is_connected = False
        self.multimeter = None
        self.update_id = None
        self.root.configure(bg='#2c3e50')

    def get_available_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports() 
                if "USB" in port.device or "COM" in port.device]
        return ports if ports else ["No ports available"]

    def toggle_connection(self):
        if not self.is_connected:
            try:
                port = self.port_combo.get()
                baud_rate = 115200
                self.multimeter = OWONXDM1041(serial_port=port, baud_rate=baud_rate)
                
                open_serial_port(self.multimeter)
                get_instrument_id(self.multimeter)
                configure_dc_voltage(self.multimeter)
                self.is_connected = True
                self.connect_button.configure(text="Disconnect")
                self.port_combo.configure(state="disabled")
                
                # Show mode buttons after successful connection
                self.dc_voltage_button.pack(side=tk.LEFT, padx=10)
                self.resistance_button.pack(side=tk.LEFT, padx=10)
                
                # Start continuous measurements
                self.start_continuous_measurement()
                
            except Exception as e:
                print(f"Connection error: {e}")
                self.multimeter = None
                
        else:
            if self.update_id:
                self.root.after_cancel(self.update_id)
                self.update_id = None
                
            if hasattr(self, 'multimeter'):
                close_serial_port(self.multimeter)
                self.multimeter = None
            self.is_connected = False
            self.connect_button.configure(text="Connect")
            self.port_combo.configure(state="normal")
            
            self.dc_voltage_button.pack_forget()
            self.resistance_button.pack_forget()
            
            self.value_display.configure(text="0.000")

if __name__ == "__main__":
    root = tk.Tk()
    app = OwonGUI(root)
    root.mainloop()