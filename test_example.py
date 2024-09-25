import time
from OWON_XDM1041 import OWONXDM1041

# time cop
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n'{func.__name__}' executed in {execution_time:.4f} seconds")
        return result
    return wrapper


@timing
def get_instrument_id(multimeter):
    return multimeter.query_instrument_id()

@timing
def configure_dc_voltage(multimeter):
    multimeter.configure_dc_voltage()
    time.sleep(3) # needed for the instrument to stabilize before measuring

@timing
def configure_resistance(multimeter):
    multimeter.configure_resistance()
    time.sleep(3) # needed for the instrument to stabilize before measuring

@timing
def measure_value(multimeter):
    return multimeter.measure_value()


@timing
def open_serial_port(multimeter):
    return multimeter.open_serial_port()

@timing
def close_serial_port(multimeter):
    return multimeter.close_serial_port()


# main sequence
if __name__ == "__main__":
    total_start_time = time.time()

    multimeter = OWONXDM1041()  # "/dev/ttyUSB0"
    open_serial_port(multimeter)
    
    print("Instrument ID:", get_instrument_id(multimeter))
    
    configure_dc_voltage(multimeter)
    measuredValue = measure_value(multimeter)
    print("Measured value:", measuredValue,"\n")

    configure_resistance(multimeter)

    loop_start_time = time.time()
    for i in range(50): # measure 50 times
        measuredValue = measure_value(multimeter)
        print(f"Measured value {i + 1}: {measuredValue}\n")

    loop_end_time = time.time()
    loop_execution_time = loop_end_time - loop_start_time
    print(f"\nFor loop executed in {loop_execution_time:.4f} seconds")

    close_serial_port(multimeter)




    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    print(f"=====Total script execution time: {total_execution_time:.4f} seconds")
