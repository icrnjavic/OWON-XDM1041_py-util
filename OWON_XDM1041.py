import serial
import time

class OWONXDM1041:
    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=115200, timeout=1):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout

    def open_serial_port(self):
        return serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)

    def query_instrument_id(self):
        try:
            ser = self.open_serial_port()
            command = b'*IDN?\n'  
            ser.write(command)
            time.sleep(3)  
            response = ser.readline().strip()
            response_text = response.decode('utf-8', errors='ignore').strip()
            #print(f"{response_text}")
            ser.close()  
            return response_text
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
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
            ser = self.open_serial_port()
            ser.write(command)
            ser.close()
            time.sleep(3)
        except serial.SerialException as e:
            return f"Failed to open serial port: {e}"

    def measure_value(self):
        try:
            ser = self.open_serial_port()
            command = b'MEAS:SHOW?\n'
            ser.write(command)
            response = ser.readline().strip()
            response_text = response.decode('utf-8', errors='ignore').strip()
            ser.close()
            return response_text
        except serial.SerialException as e:
            return f"Failed to open serial port: {e}"


