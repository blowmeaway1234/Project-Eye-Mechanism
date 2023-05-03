import serial 

ser = serial.Serial('COM3', 115200, timeout=1)
while True:
    STM32=ser.write(b'1')
    print(STM32)