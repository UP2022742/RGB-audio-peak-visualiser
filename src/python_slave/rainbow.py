import board
import neopixel
import time
import yaml
import sys

class GetAudio:
    def __init__(self):
        """ Sends volume over a socket.
        
        Loopsback the audio from the output device.
        reads the stream and gets a EMS value which
        is then sent over a RPC stream.

        Args:
            ip : The IP of the computer in which is
            hosting this application. Needed to bind
            a socket. (default: 192.168.1.222)

            port : The port in which the RPC is going
            to connect to, this must be allowed on the
            firewall for Windows computers. 
            (default: 5556)

            protocol : The protocol used to connect to
            the server, this can't be changed without
            changing the code as UDP isn't supported yet.
            (default: TCP)

            rpc_stream : the configuration in which the
            rpc stream is set.
        """
        self.pixel_pin = board.D18 # pylint: disable=no-member
        self.num_pixels = 300
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.3, auto_write=False)
        self.lights_active = True

    def signal_handler(self, sig, frame):
        """ Graceful shutdown.

        On Ctrl+C close the stream and disconnect from
        the RPC client.
        """
        self.lights_active = False
        sys.exit(0)

    def wheel(self, pos):
            if pos < 0 or pos > 255:
                return (0, 0, 0)
            if pos < 85:
                return (255 - pos * 3, pos * 3, 0)
            if pos < 170:
                pos -= 85
                return (0, 255 - pos * 3, pos * 3)
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)
        
    def rainbow_cycle(self, delay):
        for j in range(255):
            for i in range(self.num_pixels):
                rc_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(rc_index & 255)
            self.pixels.show()
            time.sleep(delay)

    def main(self):
        while self.lights_active:
            self.rainbow_cycle(0.0001)

if __name__ == "__main__":
    with open("listener.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    GetAudio().main()

    # WORKS PERFECTLY.