import board
import neopixel
pixel_pin = board.D18 # pylint: disable=no-member
num_pixels = 300
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)
pixels.fill((0,0,0))
pixels.show()
