import smbus
import csv
import datetime

def main():
    '''Returns readings for all sensors'''

    DEVICE_BUS = 1
    DEVICE_ADDR = 0x17

    TEMP_REG = 0x01
    LIGHT_REG_L = 0x02
    LIGHT_REG_H = 0x03
    STATUS_REG = 0x04
    ON_BOARD_TEMP_REG = 0x05
    ON_BOARD_HUMIDITY_REG = 0x06
    ON_BOARD_SENSOR_ERROR = 0x07
    BMP280_TEMP_REG = 0x08
    BMP280_PRESSURE_REG_L = 0x09
    BMP280_PRESSURE_REG_M = 0x0A
    BMP280_PRESSURE_REG_H = 0x0B
    BMP280_STATUS = 0x0C
    HUMAN_DETECT = 0x0D

    bus = smbus.SMBus(DEVICE_BUS)

    aReceiveBuf = []

    aReceiveBuf.append(0x00)

    for i in range(TEMP_REG,HUMAN_DETECT + 1):
        aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

    # --- Read OFF-CHIP TEMPERATURE SENSOR
    if aReceiveBuf[STATUS_REG] & 0x01 :
        print("Off-chip temperature sensor overrange!")
        T = ''
    elif aReceiveBuf[STATUS_REG] & 0x02 :
        print("No external temperature sensor!")
        T = ''
    else :
        print("Current off-chip sensor temperature = %d Celsius" % aReceiveBuf[TEMP_REG])
        T = aReceiveBuf[TEMP_REG]


    # --- Read ON-BOARD BRIGHTNESS SENSORS
    if aReceiveBuf[STATUS_REG] & 0x04 :
        print("Onboard brightness sensor overrange!")
        L = ''
    elif aReceiveBuf[STATUS_REG] & 0x08 :
        print("Onboard brightness sensor failure!")
        L = ''
    else :
        print("Current onboard sensor brightness = %d Lux" % (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]))
        L = (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])

    # --- Read ON-BOARD TEMP
    print("Current onboard sensor temperature = %d Celsius" % aReceiveBuf[ON_BOARD_TEMP_REG])
    T2 = aReceiveBuf[ON_BOARD_TEMP_REG]

    # --- Read ON-BOARD HUMIDITY
    print("Current onboard sensor humidity = %d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])
    H = aReceiveBuf[ON_BOARD_HUMIDITY_REG]

    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
        print("Onboard temperature and humidity sensor data may not be up to date!")
        T2 = ''
        H = ''

    # --- Read BAROMETER TEMP AND PRES
    if aReceiveBuf[BMP280_STATUS] == 0 :
        print("Current barometer temperature = %d Celsius" % aReceiveBuf[BMP280_TEMP_REG])
        T3 = aReceiveBuf[BMP280_TEMP_REG]
        print("Current barometer pressure = %d pascal" % (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
        P = (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16)
    else :
        print("Onboard barometer works abnormally!")
        T3 = ''
        P = ''

    if aReceiveBuf[HUMAN_DETECT] == 1 :
        print("Live body detected within 5 seconds!")
        M = 1
    else:
        print("No humans detected!")
        M = 0


    # get date and time
    x = datetime.datetime.now()

    # Write to file
    with open('/home/pi/haus_sensors/data.csv', 'a') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow([x, T, L, T2, H, T3, P, M])

    return

if __name__ == "__main__":
    main()
