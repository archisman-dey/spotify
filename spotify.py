# Arduino_LED_user.py

import serial
import time

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('COM6', 9600)

def run():
	user_input = input("\nType 1 / 2 / 3 / 4 / 5 / quit : ")
	if user_input == "1":
		print("Turning left") 
		ser.write(b'1')
		run()

	elif user_input == "2":
		print("Turning right")
		ser.write(b'2')
		run()

	elif user_input == "3":
		print("Forward")
		ser.write(b'3')
		run()

	elif user_input == "4":
		print("Back")
		ser.write(b'4')
		run()

	elif user_input == "5":
		print("Stopping")
		ser.write(b'5')
		run()

	elif user_input =="quit" or user_input == "q":
		print("Program Exiting")
		ser.write(b'5')
		ser.close()

	else:
		print("Invalid input. Type on / off / quit.")
		run()

time.sleep(2) # wait for the serial connection to initialize

run()