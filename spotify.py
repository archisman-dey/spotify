# Arduino_LED_user.py

import serial
import time
import requests
import math

initial = [[0, 0, 0]]*4
final = [[0, 0]]*4
warning = False #becomes true if any coordinate is NA
bots = ()

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
	if (xi >= xf and yf >= yi):
		return math.degrees(math.atan((xi-xf)/(yf-yi))) + 180
	elif (yf >= yi and xf >= xi):
		return 360 - math.degrees(math.atan((xf-xi)/(yf-yi)))
	elif (xf >= xi and yi >= yf):
		return math.degrees(math.atan((xf-xi)/(yi-yf)))
	elif (xi >= xf and yi >= yf):
		return 180 - math.degrees(math.atan((xi-xf)/(yi-yf)))

def convert_coordinates_to_int ():
	for i in range (0, 4, 1):
		for j in range (0, 3, 1):
			if initial[i][j] == 'NA':
				warning = True
				break
			initial[i][j] = (int)(initial[i][j])
	for i in range (0, 4, 1):
		for j in range (0, 2, 1):
			final[i][j] = (int)(final[i][j])

def distance (l1, l2):
	return (l1[0] - l2[0])**2 + (l1[1]-l2[1])**2

def send_to_bot (bot_number, num):
	message = (bytes)((str)(num * 1000 + 120 + bot_number), encoding = 'utf-8')
	ser.write(message)

def assign_bots ():
	bots_temp = ()
	mindist = 23746273649236487237627364
	for i in range (1, 5, 1):
		for j in range (1, 5, 1):
			for k in range (1, 5, 1):
				for l in range (1, 5, 1):
					if i + j + k + l == 10 and i*j*k*l == 24:
						dist = distance(initial[0], final[i-1]) + distance(initial[1], final[j-1]) + distance(initial[2], final[k-1]) + distance(initial[3], final[l-1])
						print(i,j,k,l,dist)
						if (dist < mindist):
							mindist = dist
							bots_temp = (i, j, k, l)
	return bots_temp

def orient (bot_number):
	while (True):
		get_coordinates()
		convert_coordinates_to_int()
		initial_angle = initial[bot_number - 1][2]
		final_angle = angle(initial[bot_number - 1][0] , initial[bot_number - 1][1] , final[bots[bot_number - 1]][0] , final[bots[bot_number - 1]][1])
		
		if (-10 < final_angle - initial_angle or final_angle - initial_angle < 10):
			break

		left_angle = (final_angle - initial_angle)%360
		right_angle = (initial_angle - final_angle)%360

		if (left_angle < right_angle):
			while (True):
				send_to_bot(bot_number, 1)
				time.sleep(0.2)
				get_coordinates()
				convert_coordinates_to_int()
				
				initial_angle = initial[bot_number - 1][2]
				final_angle = angle(initial[bot_number - 1][0] , initial[bot_number - 1][1] , final[bots[bot_number - 1]][0] , final[bots[bot_number - 1]][1])
				
				new_left_angle = (final_angle - initial_angle)%360
				if (new_left_angle < left_angle):
					break
		else :
			while (True):
				send_to_bot(bot_number, 2)
				time.sleep(0.2)
				get_coordinates()
				convert_coordinates_to_int()
				
				initial_angle = initial[bot_number - 1][2]
				final_angle = angle(initial[bot_number - 1][0] , initial[bot_number - 1][1] , final[bots[bot_number - 1]][0] , final[bots[bot_number - 1]][1])
				
				new_right_angle = (initial_angle - final_angle)%360
				if (new_right_angle < right_angle):
					break

def move_forward_a_bit (bot_number):
	get_coordinates()
	convert_coordinates_to_int()

	dist = distance(initial[i], final[bots[i] - 1])

	while (True):
		send_to_bot(bot_number, 3)
		time.sleep(0.2)
		get_coordinates()
		convert_coordinates_to_int()

		newdist = distance(initial[i], final[bots[i] - 1])

		if (newdist < dist):
			break

def check_if_done ():
	get_coordinates()
	convert_coordinates_to_int()
	done = [False, False, False, False]
	for i in range (0, 4, 1):
		if distance(initial[i], final[bots[i] - 1]) < 100:
			done[i] = True
	return done

time.sleep(2) # wait for the serial connection to initialize

get_coordinates()
convert_coordinates_to_int()
bots = assign_bots()

while (True):
	done = check_if_done()
	if done == [True, True, True, True]:
		break

	for i in range (1, 5, 1):
		if done[i - 1] == True:
			continue
		orient(i)
		move_forward_a_bit(i)

ser.close()