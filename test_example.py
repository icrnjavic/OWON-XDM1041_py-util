import time
from OWON_XDM1041 import OWONXDM1041

# logging function
def log_output(message):
    with open("pyvisa_log5.txt", "a") as log_file:
        log_file.write(message + "\n")

# time cop with logging
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        log_message = f"'{func.__name__}' executed in {execution_time:.4f} seconds"
        print(log_message)
        log_output(log_message)
        return result
    return wrapper


@timing
def get_instrument_id(multimeter):
    instrument_id = multimeter.query_instrument_id()
    log_output(f"Instrument ID: {instrument_id}")
    return instrument_id

@timing
def configure_dc_voltage(multimeter):
    multimeter.configure_dc_voltage()
    log_output("Configured DC Voltage")
    time.sleep(3)  # needed for the instrument to stabilize before measuring

@timing
def configure_resistance(multimeter):
    multimeter.configure_resistance()
    log_output("Configured Resistance")
    time.sleep(3)  # needed for the instrument to stabilize before measuring

@timing
def measure_value(multimeter):
    measured_value = multimeter.measure_value()
    log_output(f"Measured value: {measured_value}")
    return measured_value

@timing
def open_serial_port(multimeter):
    result = multimeter.open_serial_port()
    log_output("Serial port opened")
    return result

@timing
def close_serial_port(multimeter):
    result = multimeter.close_serial_port()
    log_output("Serial port closed")
    return result

# main sequence
if __name__ == "__main__":
    total_start_time = time.time()
    log_output("===== Script started =====")

    multimeter = OWONXDM1041()  # "/dev/ttyUSB0"
    open_serial_port(multimeter)
    
    instrument_id = get_instrument_id(multimeter)
    print("Instrument ID:", instrument_id)
    
    configure_dc_voltage(multimeter)
    measured_value = measure_value(multimeter)
    print("Measured value:", measured_value, "\n")

    configure_resistance(multimeter)

    loop_start_time = time.time()
    for i in range(50):  # measure 50 times
        measured_value = measure_value(multimeter)
        print(f"Measured value {i + 1}: {measured_value}\n")
        log_output(f"Measured value {i + 1}: {measured_value}")

    loop_end_time = time.time()
    loop_execution_time = loop_end_time - loop_start_time
    print(f"\nFor loop executed in {loop_execution_time:.4f} seconds")
    log_output(f"For loop executed in {loop_execution_time:.4f} seconds")

    close_serial_port(multimeter)

    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    print(f"===== Total script execution time: {total_execution_time:.4f} seconds")
    log_output(f"===== Total script execution time: {total_execution_time:.4f} seconds")
    log_output("===== Script ended =====")
