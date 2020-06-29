# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
    
    
# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18 # pylint: disable=no-member
    
# The number of NeoPixels
num_pixels = 300
    
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
    
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
)
    
def fill(red,green,blue):
    pixels.fill((red,green,blue))
    pixels.show()

while True:
    fill(255,0,0)
    time.sleep(0.1)
    fill(255,165,0)
    time.sleep(0.1)
    fill(255,255,0)
    time.sleep(0.1)
    fill(0,255,0)
    time.sleep(0.1)
    fill(0,0,255)
    time.sleep(0.1)
    fill(75,0,130)
    time.sleep(0.1)
    fill(238,130,221)
    time.sleep(0.1)

    # FOR TESTING PURPOSES, VERY BORING.