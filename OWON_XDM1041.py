import pyvisa
import time

class OWONXDM1041:
    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=115200, timeout=5000):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.rm = pyvisa.ResourceManager('@py') # visa-py backend to configure the port
        self.instr = None 

    def open_serial_port(self):
        if self.instr is None:  # open if not already open
            try:
                resource_address = f'ASRL{self.serial_port}::INSTR'  # /dev/ttyUSB0
                self.instr = self.rm.open_resource(resource_address)
                self.instr.baud_rate = self.baud_rate 
                self.instr.timeout = self.timeout 
                self.instr.write_termination = '\n' 
                self.instr.read_termination = '\n'
                print(f"Serial port {self.serial_port} opened.")
            except pyvisa.VisaIOError as e:
                print(f"Failed to open serial port: {e}")
                self.instr = None 
        else:
            print("Serial port is already open.")

    def close_serial_port(self):
        if self.instr is not None:
            self.instr.close()
            self.instr = None
            print("Serial port closed.")
        else:
            print("Serial port is not open.")

    def query_instrument_id(self):
        try:
            if self.instr:
                command = '*IDN?\n'
                self.instr.write(command) 
                time.sleep(0.1) 
                response = self.instr.read_raw().strip()  
                response_text = response.decode('utf-8', errors='ignore').strip() 
                return response_text
        except pyvisa.VisaIOError as e:
            print(f"Error during communication: {e}")
            return "None"

    def configure_dc_voltage(self):
        return self._configure_measurement('CONF:VOLT:DC AUTO\n')

    def configure_capacitance(self):
        return self._configure_measurement('CONF:CAP AUTO\n')

    def configure_dc_current(self):
        return self._configure_measurement('CONF:CURR:DC AUTO\n')

    def configure_temperature(self):
        return self._configure_measurement('CONF:TEMP:RTD PT100\n')
    
    def configure_temperature_unit(self):
        return self._configure_measurement('CONF:RTD:UNIT C\n')

    def configure_resistance(self):
        return self._configure_measurement('CONF:RES AUTO\n')

    def configure_frequency(self):
        return self._configure_measurement('CONF:FREQ\n')

    def configure_diode(self):
        return self._configure_measurement('CONF:DIOD\n')

    def configure_continuity(self):
        return self._configure_measurement('CONF:CONT\n')

    def _configure_measurement(self, command):
        try:
            if self.instr:
                self.instr.write(command)
                time.sleep(0.1)  
        except pyvisa.VisaIOError as e:
            return f"Error during communication: {e}"

    def measure_value(self):
        try:
            if self.instr:
                command = 'MEAS:SHOW?\n'
                self.instr.write(command)
                response = self.instr.read_raw().strip() 
                response_text = response.decode('utf-8', errors='ignore').strip()  
        except pyvisa.VisaIOError as e:
            return f"Error during communication: {e}"
