import serial
import time
import requests
import math

initial_str = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
final_str = [[0,0],[0,0],[0,0],[0,0]]
initial = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
final = [[0,0],[0,0],[0,0],[0,0]]

bots = ()
max_tries_orient = 25
max_tries_forward = 3
delay_after_send = 2
na = []

# 640 by 480, angle between 0 and 360
# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
url = "http://10.42.0.1:8080/data.txt"
ser = serial.Serial('COM6', 9600)
print("Connected to Serial")

def get_coordinates ():
	print("Get coordinates called")
	r = requests.get(url)
	string = (str)(r.content).strip("b'")

	print(string)

	initial_temp = (string.split('=')[0]).split('-')
	final_temp = (string.split('=')[1]).split('-')

	for i in range (0, 4, 1):
		initial_str[i] = [initial_temp[i].split(',')[0] , initial_temp[i].split(',')[1] , initial_temp[i].split(',')[2]]
		final_str[i] = [final_temp[i].split(',')[0] , final_temp[i].split(',')[1]]

def angle (xi, yi, xf, yf):
	print("Finding angle between : ")
	print(xi, yi, xf, yf)
	result = 0
	if xf == xi:
		if yi > yf:
			result = 90
		else:
			result = 270
	elif (xi >= xf and yf >= yi):
		result = math.degrees(math.atan((yf-yi)/(xi-xf))) + 180
	elif (yf >= yi and xf >= xi):
		result = 360 - math.degrees(math.atan((yf-yi)/(xf-xi)))
	elif (xf >= xi and yi >= yf):
		result = math.degrees(math.atan((yi-yf)/(xf-xi)))
	elif (xi >= xf and yi >= yf):
		result = 180 - math.degrees(math.atan((yi-yf)/(xi-xf)))
	print("Angle is ")
	print(result)
	return result

def convert_coordinates_to_int ():
	global na
	na = []
	for i in range (0, 4, 1):
		for j in range (0, 3, 1):
			if initial_str[i][j] == 'NA':
				na.append(i + 1)
				break
			initial[i][j] = (int)(initial_str[i][j])
	for i in range (0, 4, 1):
		for j in range (0, 2, 1):
			final[i][j] = (int)(final_str[i][j])

	if not na == []:
		react_to_NA()

def react_to_NA():
	print("Bot " + (str)(na) + " is showing NA")
	message = [5,5,5,5]
	for bot_number in na:
		angle = initial[bot_number - 1][2]
		corners = [[0,0],[480,0],[0,640],[480,640]]
		mindist = 127367123586125
		mindist_index = 0
		for i in range(0, 4, 1):
			dist = distance(initial[bot_number - 1] , corners[i])
			if dist < mindist :
				mindist = dist
				mindist_index = i

		print("Nearest to corner : " + str(corners[mindist_index]))

		if mindist_index == 0 :
			if abs(angle - 45) < 45 : #0 to 90
				print("right and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 2
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 135) < 45 : #90 to 180
				print("back")
				message = [5,5,5,5]
				message[bot_number - 1] = 4
				send_to_bots(message)
			elif abs(angle - 225) < 45 : #180 to 270
				print("left and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 1
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 315) < 45 : #270 to 360
				print("forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
		elif mindist_index == 1:
			if abs(angle - 45) < 45 : #0 to 90
				print("back")
				message = [5,5,5,5]
				message[bot_number - 1] = 4
				send_to_bots(message)
			elif abs(angle - 135) < 45 : #90 to 180
				print("left and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 1
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 225) < 45 : #180 to 270
				print("forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 315) < 45 : #270 to 360
				print("right and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 2
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
		elif mindist_index == 2:
			if abs(angle - 45) < 45 : #0 to 90
				print("forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 135) < 45 : #90 to 180
				print("right and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 2
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 225) < 45 : #180 to 270
				print("back")
				message = [5,5,5,5]
				message[bot_number - 1] = 4
				send_to_bots(message)
			elif abs(angle - 315) < 45 : #270 to 360
				print("left and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 1
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
		elif mindist_index == 3:
			if abs(angle - 45) < 45 : #0 to 90
				print("left and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 1
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 135) < 45 : #90 to 180
				print("forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 225) < 45 : #180 to 270
				print("right and forward")
				message = [5,5,5,5]
				message[bot_number - 1] = 2
				send_to_bots(message)
				message = [5,5,5,5]
				message[bot_number - 1] = 3
				send_to_bots(message)
			elif abs(angle - 315) < 45 : #270 to 360
				print("back")
				message = [5,5,5,5]
				message[bot_number - 1] = 4
				send_to_bots(message)

	get_coordinates()
	convert_coordinates_to_int()

def distance (l1, l2):
	print("Calculating distance between " + str(l1) + " and " + str(l2))
	return ((l1[0] - l2[0])**2 + (l1[1]-l2[1])**2)**0.5

def send_to_bots (num_list):
	print("Sending : " + (str)(num_list))
	message = (bytes)(''.join([str(elem) for elem in num_list]), encoding = 'utf-8')
	ser.write(message)

	time.sleep(delay_after_send)

def assign_bots ():
	print("Assign bots called")
	bots_temp = ()
	mindist = 2374627364923648723762
	for i in range (1, 5, 1):
		for j in range (1, 5, 1):
			for k in range (1, 5, 1):
				for l in range (1, 5, 1):
					if i + j + k + l == 10 and i*j*k*l == 24:
						dist = distance(initial[0], final[i-1]) + distance(initial[1], final[j-1]) + distance(initial[2], final[k-1]) + distance(initial[3], final[l-1])
						if (dist < mindist):
							mindist = dist
							bots_temp = (i, j, k, l)
	print(bots_temp)
	return bots_temp

def orient (already_done):
	print("Orient called")
	message = [5,5,5,5]
	global max_tries_orient
	print("Max tries orient is " + (str)(max_tries_orient))
	tries = max_tries_orient
	while tries:
		get_coordinates()
		convert_coordinates_to_int()

		initial_angle = [0,0,0,0]
		final_angle = [0,0,0,0]

		for bot_number in range (1, 5, 1):
			initial_angle[bot_number - 1] = initial[bot_number - 1][2]
			final_angle[bot_number - 1] = angle(initial[bot_number - 1][0] , initial[bot_number - 1][1] , final[bots[bot_number - 1] - 1][0] , final[bots[bot_number - 1] - 1][1])
		
		print("In orient, initial angles are" + str(initial_angle))
		print("In orient, final angles are" + str(final_angle))

		done = [False, False, False, False]
		for bot_number in range (1, 5, 1):
			if abs(final_angle[bot_number - 1] - initial_angle[bot_number - 1]) < 10:
				done[bot_number - 1] = True
		if done == [True, True, True, True]:
			break

		left_angle = [0,0,0,0]
		right_angle = [0,0,0,0]

		for bot_number in range (1, 5, 1):

			left_angle[bot_number - 1] = (final_angle[bot_number - 1] - initial_angle[bot_number - 1])%360
			right_angle[bot_number - 1] = (initial_angle[bot_number - 1] - final_angle[bot_number - 1])%360

			if (left_angle[bot_number - 1] < right_angle[bot_number - 1]):
				if not done[bot_number - 1]:
					message[bot_number - 1] = 1

			else :
				if not done[bot_number - 1]:
					message[bot_number - 1] = 2

		print(already_done)
		for bot_number in range (1, 5, 1):
			if already_done[bot_number - 1]:
				message[bot_number - 1] = 6
		
		print("In orient, message being sent is " + str(message))
		send_to_bots(message)
		tries -= 1

	max_tries_orient = 5

def move_forward_a_bit (done):
	print("Move forward a bit called")
	message = [3,3,3,3]
	global max_tries_forward
	print("Max tries forward is " + (str)(max_tries_forward))
	tries = max_tries_forward

	get_coordinates()
	convert_coordinates_to_int()

	initial_distances = [distance(initial[bot_number - 1] , final[bots[bot_number - 1] - 1]) for bot_number in range(1, 5, 1)]
	print("initial_distances are")
	print(initial_distances)

	while tries:
		for bot_number in range (1, 5, 1):
			if done[bot_number - 1]:
				message[bot_number - 1] = 5

		print("Sending to bots" + str(message))
		send_to_bots(message)

		get_coordinates()
		convert_coordinates_to_int()

		distances = [distance(initial[bot_number - 1] , final[bots[bot_number - 1] - 1]) for bot_number in range(1, 5, 1)]
		print("distances after trying to move a bit are")
		print(distances)

		for bot_number in range (1, 5, 1):
			if initial_distances[bot_number - 1] - distances[bot_number - 1]:
				message[bot_number - 1] = 6

		tries -= 1

def check_if_done ():
	print("Checking if done")
	message = [5,5,5,5]
	get_coordinates()
	convert_coordinates_to_int()
	done = [False, False, False, False]
	for i in range (0, 4, 1):
		if distance(initial[i], final[bots[i] - 1]) < 7:
			done[i] = True
			message[i] = 6
	if not message == [5,5,5,5]:
		send_to_bots(message)

	if not na == [] :
		for bot_number in na:
			done[bot_number - 1] = True 
	print(done)
	return done

time.sleep(2) # wait for the serial connection to initialize

get_coordinates()
convert_coordinates_to_int()
bots = assign_bots()

while True:
	done = check_if_done()
	orient(done)
	move_forward_a_bit(done)

ser.close()
