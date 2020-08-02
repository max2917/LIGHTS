import board
import neopixel
import socket
import time
import threading
import colorsys
import sched
from queue import Queue

pixelCount = 82
pixels = neopixel.NeoPixel(board.D18, pixelCount, auto_write = False)
animate = False
animationSpeed = 25

pixelLock = threading.Lock()
rainbowSched = sched.scheduler()

state = "rainbowChase"
param1 = 10
param2 = 0
param3 = 0

# Function on dedicated thread that communicated with lights direction
#  communication is based on the state of 4 variables (state, param1,
#  param2, param3) set by the main while loop
def control():
	global state, param1, param2, param3
	prevStatic = (param1, param2, param3)
	while True:
		print("* ", state, " ", param1, " ", param2, " ", param3)

		# Fill with static color
		if (state == "static"):
			# Pride is dependent on this method of rejectiong unnecessary updates
			if (param1 != prevStatic[0] or param2 != prevStatic[1] or param3 != prevStatic[2]):
				with pixelLock: pixels.fill((param1, param2, param3))
				prevStatic = (param1, param2, param3)
				pixels.show()

		# Quick flashing white
		elif (state == "strobe"):
			with pixelLock: pixels.fill((0, 0, 0))
			pixels.show()
			time.sleep(0.1)
			with pixelLock: pixels.fill((255, 255, 255))
			pixels.show()

		# Animate entire strip through rainbow
		elif (state == "rainbow"):
			# Animate entire bar (with fill) through the rainbow at speed in seconds
			for hueIndex in range(0, 100):
				if (state != "rainbow"): continue
				rgb = colorsys.hsv_to_rgb(hueIndex/100, 1, 1)
				pixels.fill((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))
				pixels.show()

		# Animate rainbow sliding across strip
		elif (state == "rainbowChase"):
			# Animate bar with rainbow
			# i is used to track the offset of the rainbow and shift it along the strip each
			#  time the while loop is run
			# the for loop is using j to paint the rainbow across the strip with i offset
			offset = 0
			while (state == "rainbowChase"):
				speedScale = 15#param1
				speedScale = int(speedScale)
				for i in range(0, pixelCount*speedScale):
					# Loop through the entire strip to fill it with the current rainbow state
					if (state != "rainbowChase"): continue # Use continue, not break.
					if ((i % speedScale) == 0):
						if (i <= (pixelCount*speedScale)): rgb = colorsys.hsv_to_rgb((i+offset)/(pixelCount*speedScale), 1, 1)
						with pixelLock: pixels[int(i/speedScale)] = (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))
				pixels.show()
				if (offset < (pixelCount*speedScale)): offset += 1
				else: offset = 0

		# Fill strip with pride flag
		elif (state == "pride"):
			# Prevent Pride from constantly refersheing the strip as it paints a "static" image
			# set state to static to utilize it's rejection properties
			# prevStatic is set to an invalid input and thus cannot be equal to a previously
			#  received input for static, current state is set to static, and param1, 2, and 3
			#  are set to the same invalid input to prevent static from attempting to write them
			#  to the lights.
			param1 = 256
			param2 = 256
			param3 = 256
			prevStatic = (256, 256, 256)
			state = "static"

			segments = 6						# number of segments to create
			leftover = pixelCount % segments	# find rounding error in pixelCount/segments
			pixelIndex = 0						# current pixel index

			for currSegment in range(0, 6):
				stripSize = (pixelCount/6)
				if (currSegment < leftover):
					stripSize += 1
				for j in range(0, int(stripSize)):
					if (currSegment == 0):
						with pixelLock: pixels[pixelIndex] = (250, 0, 0)
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

		# Police car lighting effect
		elif (state == "police"):
			animationIndex = 0	# Animation counter

			while (state == "police"):
				segments = 8						# number of segments to create
				leftover = pixelCount % segments	# find rounding error in pixelCount/segments
				pixelIndex = 0						# current pixel index

				# Divide the strip into segments
				for currSegment in range(0, segments):

					# cancel animation
					if (state != "police"): continue

					# account for rounding error
					stripSize = (pixelCount/segments)
					if (currSegment < leftover):
						stripSize += 1

					for j in range(0, int(stripSize)):
						# Fill each segment
						if (currSegment == 0):
							if ((animationIndex >= 0 and animationIndex <= 4) or (animationIndex >= 27 and animationIndex <= 30) or (animationIndex >= 32 and animationIndex <= 35) or animationIndex == 68 or animationIndex == 70):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 10 or (animationIndex >= 12 and animationIndex <= 14) or animationIndex == 16 or animationIndex == 18 or (animationIndex >= 20 and animationIndex <= 22) or animationIndex == 45 or animationIndex == 46 or animationIndex == 49 or animationIndex == 51 or (animationIndex >= 53 and animationIndex <= 56)):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 1):
							if (animationIndex == 0 or animationIndex == 2 or animationIndex == 3 or animationIndex == 31 or animationIndex == 33 or animationIndex == 35 or (animationIndex >= 37 and animationIndex <= 40) or animationIndex == 66 or animationIndex == 68 or animationIndex == 70):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 9 or animationIndex == 11 or animationIndex == 15 or (animationIndex >= 18 and animationIndex <= 20) or animationIndex == 48 or animationIndex == 50 or animationIndex == 52 or animationIndex == 54 or animationIndex == 56 or animationIndex == 57):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 2):
							if (animationIndex == 0 or (animationIndex >= 2 and animationIndex <= 4) or animationIndex == 10 or animationIndex == 12 or animationIndex == 14 or (animationIndex >= 16 and animationIndex <= 19) or animationIndex == 32 or (animationIndex >= 34 and animationIndex <= 40) or animationIndex == 50 or animationIndex == 52 or animationIndex == 54 or (animationIndex >= 56 and animationIndex <= 58) or animationIndex == 68 or animationIndex == 70):
								with pixelLock: pixels[pixelIndex] = (255, 255, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 3):
							if (animationIndex == 30 or animationIndex == 32 or animationIndex == 34 or animationIndex == 36 or animationIndex == 38 or animationIndex == 40 or animationIndex == 63 or animationIndex == 65 or animationIndex == 67 or (animationIndex >= 69 and animationIndex <= 71)):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 12 or animationIndex == 14 or (animationIndex >= 16 and animationIndex <= 18) or animationIndex == 20 or animationIndex == 47 or animationIndex == 49 or animationIndex == 51 or (animationIndex >= 53 and animationIndex <= 55)):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 4):
							if (animationIndex == 2 or animationIndex == 4 or animationIndex == 6 or (animationIndex >= 8 and animationIndex <= 10) or animationIndex == 39 or animationIndex == 41 or (animationIndex >= 43 and animationIndex <= 45)):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 18 or animationIndex == 20 or animationIndex == 22 or (animationIndex >= 24 and animationIndex <= 26) or animationIndex == 57 or animationIndex == 59 or animationIndex == 61 or animationIndex == 63 or animationIndex == 65 or animationIndex == 67):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 5):
							if (animationIndex == 5 or animationIndex == 7 or animationIndex == 9 or (animationIndex >= 11 and animationIndex <= 13) or animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or (animationIndex >= 29 and animationIndex <= 31) or animationIndex == 37 or animationIndex == 39 or animationIndex == 41 or (animationIndex >= 43 and animationIndex <= 46) or animationIndex == 59 or (animationIndex >= 61 and animationIndex <= 67)):
								with pixelLock: pixels[pixelIndex] = (255, 255, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 6):
							if (animationIndex == 3 or animationIndex == 5 or animationIndex == 7 or animationIndex == 9 or animationIndex == 11 or animationIndex == 12 or animationIndex == 36 or animationIndex == 38 or animationIndex == 42 or (animationIndex >= 45 and animationIndex <= 47) ):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 21 or animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or animationIndex == 29 or animationIndex == 30 or animationIndex == 58 or animationIndex == 60 or animationIndex == 62 or (animationIndex >= 64 and animationIndex <= 67)):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						elif (currSegment == 7):
							if (animationIndex == 0 or animationIndex == 1 or animationIndex == 4 or animationIndex == 6 or (animationIndex >= 8 and animationIndex <= 11) or animationIndex == 37 or (animationIndex >= 39 and animationIndex <= 41) or animationIndex == 43 or animationIndex == 45 or (animationIndex >= 47 and animationIndex <= 49) ):
								with pixelLock: pixels[pixelIndex] = (255, 0, 0)
							elif (animationIndex == 23 or animationIndex == 25 or animationIndex == 27 or (animationIndex >= 27 and animationIndex <= 31) or (animationIndex >= 54 and animationIndex <= 57) or (animationIndex >= 59 and animationIndex <= 62)):
								with pixelLock: pixels[pixelIndex] = (0, 0, 255)
							else:
								with pixelLock: pixels[pixelIndex] = (0, 0, 0)
						pixelIndex += 1

				# Increment animations and loop
				animationIndex += 1
				if (animationIndex > 71): animationIndex = 0

				pixels.show()
				time.sleep(0.03)

		# Fire truck lighting effect
		elif (state == "fire"):
			animationIndex = 0	# Animation counter

			while (state == "fire"):
				segments = 10						# number of segments to create
				leftover = pixelCount % segments	# find rounding error in pixelCount/segments
				pixelIndex = 0							# current pixel index

				# Divide the strip into segments
				for currSegment in range(0, segments):

					# cancel animation
					if (state != "fire"): continue

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
	control()		# Launching thread
	q.task_done()	# Exiting program

q = Queue()

t = threading.Thread(target = threader)
t.daemon = True
t.start()

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
					state = d[0]
					param1 = int(float(d[1]))
					param2 = int(float(d[2]))
					param3 = int(float(d[3]))
					print("***** ", state, " * ", param1, param2, param3, " *****")

#					elif (threading.activeCount() > 1 and d[0] != "speed"):
#						 Else, switching mode, stop any threads
#						print("ACTIVE THREADS")
#						threads = threading.enumerate()	# Get list of active threads
#						for t in threads:
#							t.join()