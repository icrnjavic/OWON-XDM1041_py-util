import serial
import time

class OWONXDM1041:
    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=115200, timeout=1):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None  # serial initialized as None

    def open_serial_port(self):
        if self.ser is None:  # open if not already open
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
                print(f"Serial port {self.serial_port} opened.")
            except serial.SerialException as e:
                print(f"Failed to open serial port: {e}")
                self.ser = None  # Reset to None if there's an error
        else:
            print("Serial port is already open.")

    def close_serial_port(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
            print("Serial port closed.")
        else:
            print("Serial port is not open.")

    def query_instrument_id(self):
        try:
            if self.ser:
                command = b'*IDN?\n'
                self.ser.write(command)
                #time.sleep(3)
                response = self.ser.readline().strip()
                response_text = response.decode('utf-8', errors='ignore').strip()
                return response_text
        except serial.SerialException as e:
            print(f"Error during communication: {e}")
            return "None"

    def configure_dc_voltage(self):
        return self._configure_measurement(b'CONF:VOLT:DC AUTO\n')

    def configure_capacitance(self):
        return self._configure_measurement(b'CONF:CAP AUTO\n')

    def configure_dc_current(self):
        return self._configure_measurement(b'CONF:CURR:DC AUTO\n')

    def configure_temperature(self):
        return self._configure_measurement(b'CONF:TEMP:RTD PT100\n')
    
    def configure_temperature_unit(self):
        return self._configure_measurement(b'CONF:RTD:UNIT C\n')

    def configure_resistance(self):
        return self._configure_measurement(b'CONF:RES AUTO\n')

    def configure_frequency(self):
        return self._configure_measurement(b'CONF:FREQ\n')

    def configure_diode(self):
        return self._configure_measurement(b'CONF:DIOD\n')

    def configure_continuity(self):
        return self._configure_measurement(b'CONF:CONT\n')

    def _configure_measurement(self, command):
        try:
            if self.ser:
                self.ser.write(command)
                #time.sleep(3)
        except serial.SerialException as e:
            return f"Error during communication: {e}"

    def measure_value(self):
        try:
            if self.ser:
                command = b'MEAS:SHOW?\n'
                self.ser.write(command)
                response = self.ser.readline().strip()
                response_text = response.decode('utf-8', errors='ignore').strip()
                return response_text
        except serial.SerialException as e:
            return f"Error during communication: {e}"
