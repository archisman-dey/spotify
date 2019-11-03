# Arduino_LED_user.py

import serial
import time
import requests
import math

initial = [[0, 0, 0]]*4
final = [[0, 0]]*4
bots = ()
max_tries_orient = 25
max_tries_forward = 3
delay_after_send = 2

# 640 by 480, angle between 0 and 360
# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
url = "http://10.150.39.190:8080/data.txt"
ser = serial.Serial('COM6', 9600)

def get_coordinates ():
	r = requests.get(url)
	string = (str)(r.content).strip("b'")

	initial_temp = (string.split('=')[0]).split('-')
	final_temp = (string.split('=')[1]).split('-')

	for i in range (0, 4, 1):
		initial[i] = [initial_temp[i].split(',')[0] , initial_temp[i].split(',')[1] , initial_temp[i].split(',')[2]]
		final[i] = [final_temp[i].split(',')[0] , final_temp[i].split(',')[1]]

def angle (xi, yi, xf, yf):
	if(xf == xi):
		if(yi > yf):
			return 90
		else:
			return 270
	if (xi >= xf and yf >= yi):
		return math.degrees(math.atan((yf-yi)/(xi-xf))) + 180
	elif (yf >= yi and xf >= xi):
		return 360 - math.degrees(math.atan((yf-yi)/(xf-xi)))
	elif (xf >= xi and yi >= yf):
		return math.degrees(math.atan((yi-yf)/(xf-xi)))
	elif (xi >= xf and yi >= yf):
		return 180 - math.degrees(math.atan((yi-yf)/(xi-xf)))

def convert_coordinates_to_int ():
	for i in range (0, 4, 1):
		for j in range (0, 3, 1):
			if initial[i][j] == 'NA':
				react_to_NA(i + 1)
			initial[i][j] = (int)(initial[i][j])
	for i in range (0, 4, 1):
		for j in range (0, 2, 1):
			final[i][j] = (int)(final[i][j])

def react_to_NA(bot_number):


def distancesq (l1, l2):
	return (l1[0] - l2[0])**2 + (l1[1]-l2[1])**2

def send_to_bots (num_list):
	message = (bytes)(''.join([str(elem) for elem in num_list]), encoding = 'utf-8')
	ser.write(message)
	time.sleep(delay_after_send)

def assign_bots ():
	bots_temp = ()
	mindist = 23746273649236487237627364
	for i in range (1, 5, 1):
		for j in range (1, 5, 1):
			for k in range (1, 5, 1):
				for l in range (1, 5, 1):
					if i + j + k + l == 10 and i*j*k*l == 24:
						dist = distancesq(initial[0], final[i-1]) + distancesq(initial[1], final[j-1]) + distancesq(initial[2], final[k-1]) + distancesq(initial[3], final[l-1])
						if (dist < mindist):
							mindist = dist
							bots_temp = (i, j, k, l)
	return bots_temp

def orient ():
	message = [5]*4
	tries = max_tries_orient
	while tries:
		get_coordinates()
		convert_coordinates_to_int()

		initial_angle = [0]*4
		final_angle = [0]*4

		for bot_number in range (1, 5, 1):
			initial_angle[bot_number - 1] = initial[bot_number - 1][2]
			final_angle[bot_number - 1] = angle(initial[bot_number - 1][0] , initial[bot_number - 1][1] , final[bots[bot_number - 1] - 1][0] , final[bots[bot_number - 1] - 1][1])
		
		done = [False]*4
		for bot_number in range (1, 5, 1):
			if abs(final_angle[bot_number - 1] - initial_angle[bot_number - 1]) < 10:
				done[bot_number - 1] = True
		if done == [True]*4:
			break

		left_angle = [0]*4
		right_angle = [0]*4

		for bot_number in range (1, 5, 1):

			left_angle[bot_number - 1] = (final_angle[bot_number - 1] - initial_angle[bot_number - 1])%360
			right_angle[bot_number - 1] = (initial_angle[bot_number - 1] - final_angle[bot_number - 1])%360

			if (left_angle[bot_number - 1] < right_angle[bot_number - 1]):
				if not done[bot_number - 1]:
					message[bot_number - 1] = 1

			else :
				if not done[bot_number - 1]:
					message[bot_number - 1] = 2

		send_to_bots(message)
		tries -= 1

	max_tries_orient = 5


def move_forward_a_bit (bot_number):
	message = [3]*4
	tries = max_tries_forward

	get_coordinates()
	convert_coordinates_to_int()

	initial_distances = [distancesq(initial[bot_number - 1] , final[bots[bot_number - 1] - 1]) for bot_number in range(1, 5, 1)]

	while tries:
		send_to_bots(message)

		get_coordinates()
		convert_coordinates_to_int()

		distances = [distancesq(initial[bot_number - 1] , final[bots[bot_number - 1] - 1]) for bot_number in range(1, 5, 1)]

		for bot_number in (1, 5, 1):
			if initial_distances[bot_number - 1] - distances[bot_number - 1]:
				message[bot_number - 1] = 5

		tries -= 1

def check_if_done ():
	get_coordinates()
	convert_coordinates_to_int()
	done = [False, False, False, False]
	for i in range (0, 4, 1):
		if distancesq(initial[i], final[bots[i] - 1]) < 9:
			done[i] = True
			send_to_bot(i, 6)
	return done

time.sleep(2) # wait for the serial connection to initialize

get_coordinates()
convert_coordinates_to_int()
bots = assign_bots()

while True:
	done = check_if_done()

	for i in range (1, 5, 1):
		if done[i - 1] == True:
			continue
		orient(i)
		move_forward_a_bit(i)

"""
for i in range (1, 6, 1):
	send_to_bot(4, 3)
	time.sleep(1.25)

for i in range (1, 6, 1):
	send_to_bot(1,3)
	time.sleep(1.5)
	send_to_bot(2,3)
	time.sleep(1.5)
	send_to_bot(3,3)
	time.sleep(1.5)
"""
ser.close()
