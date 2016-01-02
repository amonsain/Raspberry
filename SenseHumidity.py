from sense_hat import SenseHat
import time

sense = SenseHat()


green = (0, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)

sense.low_light = True

while True:

 humidity = sense.humidity 
 humidity_value = 64 * humidity / 100
 print(humidity)

 pixels = [green if i < humidity_value/2 else white if i<humidity_value else red for i in range(64)]
 sense.set_pixels(pixels) 
 time.sleep(1)