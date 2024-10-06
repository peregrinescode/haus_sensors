import smbus
import sds011
import time

DEVICE_BUS = 1

# Device address
DEVICE_ADDR = 0x17
# Functions & Register addresses
TEMP_REG = 0x01                 # Ext. Temperature [Unit:degC] 
LIGHT_REG_L = 0x02              # Light Brightness Low 8 Bit [Unit:Lux]
LIGHT_REG_H = 0x03              # Light Brightness High 8 Bit [Unit:Lux] 
STATUS_REG = 0x04               # Status Function
ON_BOARD_TEMP_REG = 0x05        # OnBoard Temperature [Unit:degC] 
ON_BOARD_HUMIDITY_REG = 0x06    # OnBoard Humidity [Uinit:%] 
ON_BOARD_SENSOR_ERROR = 0x07    # 0(OK) - 1(Error) 
BMP280_TEMP_REG = 0x08          # P. Temperature [Unit:degC] 
BMP280_PRESSURE_REG_L = 0x09    # P. Pressure Low 8 Bit [Unit:Pa] 
BMP280_PRESSURE_REG_M = 0x0A    # P. Pressure Mid 8 Bit [Unit:Pa]
BMP280_PRESSURE_REG_H = 0x0B    # P. Pressure High 8 Bit [Unit:Pa] 
BMP280_STATUS = 0x0C            # 0(OK) - 1(Error) 
HUMAN_DETECT = 0x0D             # 0(No Active Body) - 1(Active Body) 

bus = smbus.SMBus(DEVICE_BUS)

aReceiveBuf = []

aReceiveBuf.append(0x00)

for i in range(TEMP_REG,HUMAN_DETECT + 1):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

if aReceiveBuf[STATUS_REG] & 0x01 :
    print("Off-chip temperature sensor overrange!")
elif aReceiveBuf[STATUS_REG] & 0x02 :
    print("No external temperature sensor!")
else :
    print("Current off-chip sensor temperature = %d Celsius" % aReceiveBuf[TEMP_REG])


if aReceiveBuf[STATUS_REG] & 0x04 :
    print("Onboard brightness sensor overrange!")
elif aReceiveBuf[STATUS_REG] & 0x08 :
    print("Onboard brightness sensor failure!")
else :
    print("Current onboard sensor brightness = %d Lux" % (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]))

print("Current onboard sensor temperature = %d Celsius" % aReceiveBuf[ON_BOARD_TEMP_REG])
print("Current onboard sensor humidity = %d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])

if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
    print("Onboard temperature and humidity sensor data may not be up to date!")

if aReceiveBuf[BMP280_STATUS] == 0 :
    print("Current barometer temperature = %d Celsius" % aReceiveBuf[BMP280_TEMP_REG])
    print("Current barometer pressure = %d pascal" % (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
else :
    print("Onboard barometer works abnormally!")

if aReceiveBuf[HUMAN_DETECT] == 1 :
    print("Live body detected within 5 seconds!")
else:
    print("No humans detected!")


# Read air quality sensor data
sds = SDS011("/dev/ttyUSB0", use_query_mode=True)
# time.sleep(15)  # Allow time for the sensor to measure properly
print(sds.query())  # Gets (pm25, pm10)
# sds.sleep()  # Turn off fan and diode