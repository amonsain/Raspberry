from sense_hat import SenseHat
import pygame
from pygame.locals import *
import subprocess

sense =  SenseHat()
RadioOn = False
PlayListLength = 4
CurrentTrack = 1

# Handle user IO on SenseHat(uses pygame), and toggles internet radio (requires mpd/mpc to be installed on your system)
# limits "mprc prev" and "mpc next" to the max number of tracks in the playlist to avoid issues when "mpc next" is called from the last track

def radio_commands(event):
	global RadioOn
	global CurrentTrack
	global PlayListLength

	if event.key == pygame.K_UP:
		subprocess.check_output(["mpc","volume","-1"])

	elif event.key == pygame.K_DOWN:
		subprocess.check_output(["mpc","volume","+1"])

	elif event.key == pygame.K_RIGHT and CurrentTrack < PlayListLength :
		status = subprocess.check_output(["mpc","next"])
		CurrentTrack= CurrentTrack+1
		print(status)

	elif event.key == pygame.K_LEFT and CurrentTrack > 1:
		status = subprocess.check_output(["mpc","prev"])
		CurrentTrack= CurrentTrack-1
		print(status)

	elif event.key == pygame.K_RETURN:
		if RadioOn:
			subprocess.check_output(["mpc","stop"])
			RadioOn = False
			
		else: 
			subprocess.check_output(["mpc","play","1"])
			RadioOn = True
			CurrentTrack = 1




def main():

	#initialize Pygame which handles joystick inputs on SenseHat
	pygame.init()
	pygame.display.set_mode((640, 480))

	subprocess.call(["mpc","clear"])
	subprocess.call(["mpc","load","playlist1"])
	subprocess.call(["mpc","enable","1"])


	# SenseHat initialization and configuration
	sense = SenseHat()
	sense.low_light = True
	sense.rotation = 90

	#initialize last weather update time
	last_update_time = 0

	#Main loop

	while True:  

		#Handle Senshat Joystick inputs
		for event in pygame.event.get():
			#if event.type == KEYDOWN:
				#radio_commands(event)
				#print('DN')
			if event.type == KEYUP:
				radio_commands(event)
				print('SenseHat Input')

if __name__=="__main__":
	main()	















