import board
import neopixel
import socket
import time
import threading
import colorsys
import sched
from queue import Queue

previousButton = "none"
pixelCount = 150
pixels = neopixel.NeoPixel(board.D18, pixelCount, auto_write = False)
animate = False

pixelLock = threading.Lock()
rainbowSched = sched.scheduler()

def rainbowChase():
	# Animate bar with rainbow
	# i is used to track the offset of the rainbow and shift it along the strip each
	#  time the while loop is run
	# the for loop is using j to paint the rainbow across the strip with i offset
	offset = 0
	while (animate == True):
		for i in range(0, pixelCount*10):
			# Loop through the entire strip to fill it with the current rainbow state
			if (animate == False): break
			if ((i % 10) == 0):
				if (i <= (pixelCount*10)): rgb = colorsys.hsv_to_rgb((i+offset)/(pixelCount*10), 1, 1)
				with pixelLock: pixels[int(i/10)] = (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))
		pixels.show()
#		time.sleep(0.05)
		if (offset < (pixelCount*10)): offset += 1
		else: offset = 0

rainbowHue = 0
rainbowTick = 0.001
rainbowSpeed = 0.001

def rainbow(speed):
	global rainbowHue, rainbowTick, rainbowSpeed
	# Animate entire bar (with fill) through the rainbow at speed in seconds (between each color)
	print("Rainbow speed: ", speed)
	if (speed == 0): speed = 0.001
	
	rainbowSpeed = speed
	rainbowHue = 0
	rainbowTick = 0.001

	def update():
		global rainbowHue, rainbowTick, rainbowSpeed

		if (not animate):
			rainbowSched.queue.clear()
			return

		rainbowSched.enter(rainbowSpeed, 1, update)
		if (((rainbowHue + rainbowTick) > 1.0) or ((rainbowHue + rainbowTick) < 0.0)):
			rainbowTick *= -1
		rainbowHue += rainbowTick
		rgb = colorsys.hsv_to_rgb(rainbowHue, 1, 1)
		with pixelLock: pixels.fill((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))
		pixels.show()

	rainbowSched.enter(rainbowSpeed, 1, update)
	rainbowSched.run()

def pride():
	print("PRIDE")
	
	leftover = pixelCount%6
	count = 0
	for i in range(0, 6):
		stripSize = (pixelCount/6)
		if (i < leftover):
			stripSize += 1
		for j in range(0, int(stripSize)):
			if (i == 0):
				with pixelLock: pixels[count] = (250, 3, 3)
			elif (i == 1):
				with pixelLock: pixels[count] = (255, 25, 0)
			elif (i == 2):
				with pixelLock: pixels[count] = (255, 175, 0)
			elif (i == 3):
				with pixelLock: pixels[count] = (0, 255, 0)
			elif (i == 4):
				with pixelLock: pixels[count] = (0, 77, 255)
			elif (i == 5):
				with pixelLock: pixels[count] = (117, 7, 135)
			count += 1
	pixels.show()

def strobe():
	print("STROBE")
	while True:
		if (animate == False): break
		with pixelLock: pixels.fill((0, 0, 0))
		pixels.show()
		time.sleep(0.1)
		if (animate == False): break
		with pixelLock: pixels.fill((255, 255, 255))
		pixels.show()

def police():

	br13 = 0
	br2 = 0
	brw = 0

	while (animate == True):
		segments = 8	# number of segments to create (switch cases will have to be altered)
		leftover = pixelCount % segments
		count = 0

		# Divide the strip into segments
		for i in range(0, segments):
			stripSize = (pixelCount/segments)
			if (i < leftover):
				stripSize += 1
			for j in range(0, int(stripSize)):
				# Fill each segment
				if (i == 0 or i == 3):
					# RED 1, 3
					if (br13 == 2 or br13 == 8 or br13 == 11 or br13 == 14 or br13 == 17):
						with pixelLock: pixels[count] = (255, 0, 0)
					else:
						with pixelLock: pixels[count] = (0, 0, 0)
				elif (i == 1):
					# RED 2
					# 12 on, 2 off, 1 on, 8 off, 1 on, 2 off, 9 on, 14 off
					if (br2 <= 11 or br2 == 14 or br2 == 23 or (br2 >= 26 and br2 <= 35) or br2 == 38 or br2 == 45):
						with pixelLock: pixels[count] = (255, 0, 0)
					else:
						with pixelLock: pixels[count] = (0, 0, 0)
				elif (i == 2 or i == 5):
					# WHITE R, B
					# 6R, 6B, 6R, 6B, 9R, 9B
					if ((brw >= 0 and brw <=5) or (brw >= 12 and brw <= 17) or (brw >= 24 and brw <= 32)):
						if (i ==2):
							with pixelLock: pixels[count] = (255, 255, 255)
						if (i == 5):
							with pixelLock: pixels[count] = (0, 0, 0)
					else:
						if (i ==2):
							with pixelLock: pixels[count] = (0, 0, 0)
						if (i == 5):
							with pixelLock: pixels[count] = (255, 255, 255)
				elif (i == 4 or i == 7):
					# BLUE 1, 3
					if (br13 == 6 or br13 == 12 or br13 == 15 or br13 == 18 or br13 == 3):
						with pixelLock: pixels[count] = (0, 0, 255)
					else:
						with pixelLock: pixels[count] = (0, 0, 0)
				elif (i == 6):
					# BLUE 2, Same as RED 2 with offset
					# 12 on, 2 off, 1 on, 8 off, 1 on, 2 off, 9 on, 14 off
					if ((br2 >= 11 and br2 <= 23) or br2 == 26 or br2 == 35 or (br2 >= 38 and br2 <= 47) or br2 == 1 or br2 == 8):
						with pixelLock: pixels[count] = (0, 0, 255)
					else:
						with pixelLock: pixels[count] = (0, 0, 0)
				count += 1

		# Increment animations and reset at strip end
		br13 += 1
		br2 += 1
		brw += 1
		if (br13 > 17): br13 = 0
		if (br2 > 48): br2 = 0
		if (brw > 41): brw = 0

		pixels.show()
		time.sleep(0.03)

def threader():
	while True:
		# Get params for this thread
		params = q.get()
		# Check animation type in params
		if (params[0] == "rainbow"):
			rainbow(int(params[1]))
			q.task_done()
		elif(params[0] == "rainbowChase"):
			rainbowChase()
			q.task_done()
		elif (params[0] == "pride"):
			pride()
			q.task_done()
		elif (params[0] == "strobe"):
			strobe()
			q.task_done()
		elif (params[0] == "police"):
			police()
			q.taks_done()
		elif (params[0] == "fire"):
			#fire()
			q.task_done()

q = Queue()

while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(("", 10250))
		print("Start listen")
		s.listen() # Wait for single on port
		conn, addr = s.accept()
		with conn:
			# Connection received
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				if not data:
					break
				if data:
					# Up to 4 parameters, d[0] is identifier flag
					d = data.decode("utf-8").split(',', 4)
					print("***** Type and values received: ",d[0], d[1], d[2], d[3], "*****")

					if (previousButton == d[0]):
						# If the same button is pressed twice, do nothing
						break
					elif (threading.activeCount() > 1):
						# Else, switching mode, stop any threads
						#print("ACTIVE THREADS")
						#threads = threading.enumerate()	# Get list of active threads
						#for t in threads:
						#	t.join()

						# Tell any animation threads to exit
						animate = False

					# Split by animation flag
					if (d[0] == "static"):
						with pixelLock: pixels.fill((int(float(d[1])), int(float(d[2])), int(float(d[3]))))
						pixels.show()
						# Previous set to "none" because this if block is not
						#  computationally expensive or fragile. It also simplifies
						#  the network packets to do it this way.
						previousButton = "none"
					elif (d[0] == "rainbow"):
						print("previous button", d[0])
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0], d[1]] # Name and speed of animation
						q.put(params)
					elif (d[0] == "rainbowChase"):
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0], d[1]] # Name and speed of animation
						q.put(params)
					elif (d[0] == "pride"):
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0]] # Name and speed of animation
						q.put(params)
					elif (d[0] == "strobe"):
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0]]
						q.put(params)
					elif (d[0] == "fire"):
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0]]
						q.put(params)
					elif (d[0] == "police"):
						previousButton = d[0]
						animate = False
						time.sleep(0.01)
						animate = True

						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()
						params = [d[0]]
						q.put(params)
