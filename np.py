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
animationSpeed = 25

pixelLock = threading.Lock()
rainbowSched = sched.scheduler()

def rainbowChase():
	# Animate bar with rainbow
	# i is used to track the offset of the rainbow and shift it along the strip each
	#  time the while loop is run
	# the for loop is using j to paint the rainbow across the strip with i offset
	offset = 0
	while (animate == True):
		speedScale = animationSpeed
		speedScale = int(speedScale)
		for i in range(0, pixelCount*speedScale):
			# Loop through the entire strip to fill it with the current rainbow state
			if (animate == False): break
			if ((i % speedScale) == 0):
				if (i <= (pixelCount*speedScale)): rgb = colorsys.hsv_to_rgb((i+offset)/(pixelCount*speedScale), 1, 1)
				with pixelLock: pixels[int(i/speedScale)] = (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))
		pixels.show()
		if (offset < (pixelCount*speedScale)): offset += 1
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


# Fill strip with pride flag
def pride():
	segments = 6						# number of segments to create
	leftover = pixelCount % segments	# find rounding error in pixelCount/segments
	pixelIndex = 0						# current pixel index

	for currSegment in range(0, 6):
		stripSize = (pixelCount/6)
		if (currSegment < leftover):
			stripSize += 1
		for j in range(0, int(stripSize)):
			if (currSegment == 0):
				with pixelLock: pixels[pixelIndex] = (250, 3, 3)
			elif (currSegment == 1):
				with pixelLock: pixels[pixelIndex] = (255, 25, 0)
			elif (currSegment == 2):
				with pixelLock: pixels[pixelIndex] = (255, 175, 0)
			elif (currSegment == 3):
				with pixelLock: pixels[pixelIndex] = (0, 255, 0)
			elif (currSegment == 4):
				with pixelLock: pixels[pixelIndex] = (0, 77, 255)
			elif (currSegment == 5):
				with pixelLock: pixels[pixelIndex] = (117, 7, 135)
			pixelIndex += 1
	pixels.show()

# Flash white quickly
def strobe():
	while True:
		if (animate == False): break
		with pixelLock: pixels.fill((0, 0, 0))
		pixels.show()
		time.sleep(0.1)
		if (animate == False): break
		with pixelLock: pixels.fill((255, 255, 255))
		pixels.show()

# Police car lighting effect
def police():

	br13 = 0
	br2 = 0
	brw = 0

	while (animate == True):
		segments = 8						# number of segments to create
		leftover = pixelCount % segments	# find rounding error in pixelCount/segments
		pixelIndex = 0						# current pixel index

		# Divide the strip into segments
		for currSegment in range(0, segments):

			# Cancel animation
			if (animate == False): break

			# Calculate stripSize and adjust segments for rounding error
			stripSize = (pixelCount/segments)
			if (currSegment < leftover):
				stripSize += 1

			for j in range(0, int(stripSize)):
				# Fill each segment
				if (currSegment == 0 or currSegment == 3):
					# RED 1, 3
					if (br13 == 2 or br13 == 8 or br13 == 11 or br13 == 14 or br13 == 17):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 1):
					# RED 2
					# 12 on, 2 off, 1 on, 8 off, 1 on, 2 off, 9 on, 14 off
					if (br2 <= 11 or br2 == 14 or br2 == 23 or (br2 >= 26 and br2 <= 35) or br2 == 38 or br2 == 45):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 2 or currSegment == 5):
					# WHITE R, B
					# 6R, 6B, 6R, 6B, 9R, 9B
					if ((brw >= 0 and brw <=5) or (brw >= 12 and brw <= 17) or (brw >= 24 and brw <= 32)):
						if (currSegment ==2):
							with pixelLock: pixels[pixelIndex] = (255, 255, 255)
						if (currSegment == 5):
							with pixelLock: pixels[pixelIndex] = (0, 0, 0)
					else:
						if (currSegment ==2):
							with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						if (currSegment == 5):
							with pixelLock: pixels[pixelIndex] = (255, 255, 255)
				elif (currSegment == 4 or currSegment == 7):
					# BLUE 1, 3
					if (br13 == 6 or br13 == 12 or br13 == 15 or br13 == 18 or br13 == 3):
						with pixelLock: pixels[pixelIndex] = (0, 0, 255)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 6):
					# BLUE 2, Same as RED 2 with offset
					# 12 on, 2 off, 1 on, 8 off, 1 on, 2 off, 9 on, 14 off
					if ((br2 >= 11 and br2 <= 23) or br2 == 26 or br2 == 35 or (br2 >= 38 and br2 <= 47) or br2 == 1 or br2 == 8):
						with pixelLock: pixels[pixelIndex] = (0, 0, 255)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				pixelIndex += 1

		# Increment animations and reset at strip end
		br13 += 1
		br2 += 1
		brw += 1
		if (br13 > 17): br13 = 0
		if (br2 > 48): br2 = 0
		if (brw > 41): brw = 0

		pixels.show()
		time.sleep(0.03)

# Fire truck lighting effect
def fire():

	animationIndex = 0	# Animation counter

	while (animate == True):
		segments = 10						# number of segments to create
		leftover = pixelCount % segments	# find rounding error in pixelCount/segments
		pixelIndex = 0							# current pixel index

		# Divide the strip into segments
		for currSegment in range(0, segments):

			# cancel animation
			if (animate == False): break

			# account for rounding error
			stripSize = (pixelCount/segments)
			if (currSegment < leftover):
				stripSize += 1

			for j in range(0, int(stripSize)):
				# Fill each segment
				if (currSegment == 0):
					if (animationIndex == 5 or (animationIndex >= 7 and animationIndex <= 12) or animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or (animationIndex >= 29 and animationIndex <= 31) or animationIndex == 42 or (animationIndex >= 44 and animationIndex <= 49) or animationIndex == 59 or animationIndex == 61 or animationIndex == 63 or (animationIndex >= 65 and animationIndex <= 68)):						
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 1):
					if (animationIndex == 3 or animationIndex == 5 or animationIndex == 7 or (animationIndex >= 9 and animationIndex <= 11) or (animationIndex >= 22 and animationIndex <= 29) or animationIndex == 40 or animationIndex == 42 or animationIndex == 44 or (animationIndex >= 46 and animationIndex <= 48) or animationIndex == 58 or animationIndex == 60 or animationIndex == 62 or (animationIndex >= 64 and animationIndex <=66)):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 2):
					if (animationIndex == 5 or animationIndex == 7 or animationIndex == 9 or (animationIndex >= 11 and animationIndex <= 13) or animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or (animationIndex >= 29 and animationIndex <= 31) or animationIndex == 42 or animationIndex == 44 or animationIndex == 46 or (animationIndex >= 48 and animationIndex <= 50) or animationIndex == 60 or (animationIndex >= 62 and animationIndex <= 68)):
						with pixelLock: pixels[pixelIndex] = (255, 255, 255)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 3):
					if (animationIndex == 5 or animationIndex == 7 or animationIndex == 9 or animationIndex == 11 or animationIndex == 12 or animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or (animationIndex >=29 and animationIndex <= 31) or animationIndex == 42 or animationIndex == 44 or animationIndex == 46 or animationIndex == 48 or animationIndex == 49 or animationIndex == 59 or animationIndex == 61 or animationIndex == 63 or (animationIndex >= 65 and animationIndex <= 68)):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 4):
					if (animationIndex == 0 or animationIndex == 2 or animationIndex == 4 or (animationIndex >= 6 and animationIndex <= 8) or animationIndex == 18 or animationIndex == 20 or animationIndex == 22 or (animationIndex >= 24 and animationIndex <= 27) or animationIndex == 37 or animationIndex == 39 or animationIndex == 41 or (animationIndex >= 43 and animationIndex <= 45) or (animationIndex >= 55 and animationIndex <= 58) or (animationIndex >= 60 and animationIndex <= 63)):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 5):
					if ((animationIndex >= 9 and animationIndex <= 12) or (animationIndex >= 14 and animationIndex <= 17) or animationIndex == 27 or animationIndex == 29 or animationIndex == 31 or (animationIndex >= 33 and animationIndex <= 35) or animationIndex == 45 or animationIndex == 47 or animationIndex == 49 or (animationIndex >= 51 and animationIndex <= 54) or animationIndex == 64 or animationIndex == 66 or animationIndex == 68 or (animationIndex >= 70 and animationIndex <= 72)):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 6):
					if (animationIndex == 0 or animationIndex == 2 or animationIndex == 3 or animationIndex == 13 or animationIndex == 15 or animationIndex == 17 or (animationIndex >= 19 and animationIndex <= 22) or animationIndex == 32 or animationIndex == 34 or animationIndex == 36  or animationIndex == 38 or animationIndex == 39 or animationIndex == 50 or animationIndex == 52 or animationIndex == 53 or animationIndex == 54 or (animationIndex >= 56 and animationIndex <= 58) or animationIndex == 69 or animationIndex == 71):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 7):
					if (animationIndex == 0 or (animationIndex >= 2 and animationIndex <= 4) or animationIndex == 14 or (animationIndex >= 16 and animationIndex <= 22) or animationIndex == 32 or animationIndex == 34 or animationIndex == 36 or (animationIndex >= 38 and animationIndex <= 40) or animationIndex == 50 or animationIndex == 52 or animationIndex == 54 or (animationIndex >= 56 and animationIndex <=58) or animationIndex == 69 or animationIndex == 71):
						with pixelLock: pixels[pixelIndex] = (255, 255, 255)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 8):
					if ((animationIndex >=0 and animationIndex <= 2) or animationIndex == 12 or animationIndex == 14 or animationIndex == 16 or (animationIndex >= 18 and animationIndex <= 20) or animationIndex == 30 or animationIndex == 32 or animationIndex == 34 or (animationIndex >= 36 and animationIndex <= 38) or (animationIndex >= 49 and animationIndex <= 56) or animationIndex == 67 or animationIndex == 69 or animationIndex == 71):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				elif (currSegment == 9):
					if ((animationIndex >= 0 and animationIndex <= 3) or animationIndex == 13 or animationIndex == 15 or animationIndex == 17 or (animationIndex >= 19 and animationIndex <= 22) or animationIndex == 32 or (animationIndex >= 34 and animationIndex <= 39) or animationIndex == 50 or animationIndex == 52 or animationIndex == 54 or (animationIndex >= 56 and animationIndex <= 58) or animationIndex == 69 or animationIndex == 71 or animationIndex == 72):
						with pixelLock: pixels[pixelIndex] = (255, 0, 0)
					else:
						with pixelLock: pixels[pixelIndex] = (0, 0, 0)
				pixelIndex += 1

		# Increment animations and loop
		animationIndex += 1
		if (animationIndex > 72): animationIndex = 0

		pixels.show()
		time.sleep(0.03)

def threader():
	while (True):
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
			fire()
			q.task_done()

q = Queue()

while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(("", 10250))
		print("Start listen")
		s.listen() # Wait for signal on port
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
					print("***** Received: ",d[0], d[1], d[2], d[3], "*****")

					if (previousButton == d[0]):
						# If the same button is pressed twice, do nothing
						break
					elif (threading.activeCount() > 1 and d[0] != "speed"):
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
					elif (d[0] == "speed"):
						# Handle speed adjustemnt for animations
						print("Animation speed change: ", d[1])
						animationSpeed = d[1]
					else:
						# Slection was an animation/function more complex than 'static'

						# Set new previous button
						previousButton = d[0]

						# REMOVE when we figure out how to cancel threads proeprly
						animate = False
						time.sleep(0.01)
						animate = True
						
						# Start threading, 
						t = threading.Thread(target = threader)
						t.daemon = True
						t.start()

					if (d[0] == "rainbow" or d[0] == "rainbowChase" or d[0] == "strobe"):
						# Animations with a speed option
						print("ANIMATE WITH SPEED ", d[1])
						params = [d[0], d[1]] # Name and speed of animation
						q.put(params)
					else:
						# Animations that don't have any user options
						params = [d[0]] # Name and speed of animation
						q.put(params)
