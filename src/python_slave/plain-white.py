import board
import neopixel

pixel_pin = board.D18 # pylint: disable=no-member
num_pixels = 300
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

pixels.fill((255,255,255))
pixels.show()