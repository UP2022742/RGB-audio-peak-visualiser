# coding: utf-8
import asyncio
import aiozmq
import zmq
import yaml
import signal
import sys
import time
import threading
import board
import neopixel
import struct

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
        self.max_pixels = 300
        self.pixel_pin = board.D18 # pylint: disable=no-member
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.max_pixels, brightness=0.1, auto_write=False, pixel_order=self.ORDER
        )
        self.protocol = cfg["RPC"]["protocol"]
        self.IP = cfg["RPC"]["IP"]
        self.port = cfg["RPC"]["port"]
        self.rpc_stream = 0
        self.output = 0
        self.lights_active = True

    def signal_handler(self, sig, frame):
        """ Graceful shutdown.

        On Ctrl+C close the stream and disconnect from
        the RPC client.
        """

        print("\nClosing RPC stream...")
        self.rpc_stream.close()
        self.lights_active = False
        sys.exit(0)
    
    def color_loop(self, i):
        switcher={
            0:(255,0,0), # Red
            1:(255,165,0), # Orange
            2:(255,255,0), # Yellow
            3:(0,255,0), # Green
            4:(0,0,255), # Blue
            5:(75,0,130), # Indigo
            6:(238,130,221), # Violet
        }
        return switcher.get(i,"[ERROR] INVALID COLOUR")

    def running_rabbit(self):
        rgb_loop = 0
        while self.lights_active:

            # Starts the index on the first light. As song gets louder keeps increasing.
            light_index = 0
            while(light_index < self.max_pixels and self.lights_active == True):
                if self.output > 0.4:
                    self.pixels[light_index] = self.color_loop(rgb_loop)
                    self.pixels.show()
                    time.sleep(0.001)
                    light_index += 1

            light_index = 0
            if rgb_loop < 6: rgb_loop += 1
            else: rgb_loop = 1
            

    async def do(self):
            self.rpc_stream = await aiozmq.stream.create_zmq_stream(
                zmq_type=zmq.SUB, # pylint: disable=no-member
                connect=self.protocol+'://'+str(self.IP)+':'+str(self.port),
            )
            self.rpc_stream.transport.subscribe(b'A')

            while True:
                msg = await self.rpc_stream.read()
                self.output = struct.unpack('d', msg[1])[0]

    def main(self):
        """ Recieves volume over socket.
        
        Receives the stream data converts the bytes
        object to a int and displays the integer.

        Args:
            msg : Reads the RPC stream, then gets
            turned from a byte object to a integer
            then displayed.
        """
        signal.signal(signal.SIGINT, self.signal_handler)

        # Create new light thread.
        try:
            lighting_sequence = threading.Thread(target=self.running_rabbit)
            lighting_sequence.start()
        except:
            print("Error: unable to start thread")

        # Start recording stream
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.do())

if __name__ == "__main__":
    with open("listener.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    GetAudio().main()

    # WORKS PERFECTLY.