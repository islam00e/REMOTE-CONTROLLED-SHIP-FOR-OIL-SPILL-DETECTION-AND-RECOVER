import serial
import time
# Replace "COM3" with your actual port
port = "COM19"
baudrate = 9600

# Open serial port
ser = serial.Serial(port, baudrate)

# Function to send commands to Arduino
def send_command(command):
    ser.write(command.encode() + "\n".encode())

# Turn LED on
send_command("ON")

# Wait for 5 seconds
time.sleep(10)

# Turn LED off
send_command("OFF")

# Close serial port
ser.close()
