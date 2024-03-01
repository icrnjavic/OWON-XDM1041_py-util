from OWON_XDM1041 import OWONXDM1041

multimeter = OWONXDM1041() # Port defaults to "/dev/ttyUSB0"

# Get instrument ID
print("Instrument ID:", multimeter.query_instrument_id())

# Configure DC voltage
multimeter.configure_dc_voltage()


# Measure value of the set config
measuredValue = multimeter.measure_value()
print("Measured value:", measuredValue)
