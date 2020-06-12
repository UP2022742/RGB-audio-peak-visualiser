import pyaudio
import sys
# import numpy as np
import zmq
import asyncio
import aiozmq
import yaml
from socket import gethostbyname, gethostname
import signal
import audioop

class GetAudio:
    """ Sends volume over a socket.
        
    Loopsback the audio from the output device.
    reads the stream and gets a EMS value which
    is then sent over a RPC stream.

    Args:
        p : A variable to access PyAudio functions.

        device_set : Used to check weather a valid
        device has been applied yet.

        device_info : Contains the array of 
        hardware information that is required
        when setting up the audio stream.

        default_frames : Audio sampling rate.
        (default: 512)

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

        chunk : Number of frames signal is split by
        typically the smaller the faster the code
        runs (default: 2048)

        device_selection : Takes the users input
        and converts it to an integer so it can
        be validated against.

        rpc_stream : the configuration in which the
        rpc stream is set.
    """
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_set = False
        self.device_info = {}
        self.default_frames = cfg["stream"]["defaultframes"] 
        self.ip = "192.168.1.214"
        self.port = cfg["RPC"]["port"]
        self.protocol = cfg["RPC"]["protocol"]
        self.chunk = cfg["stream"]["CHUNK"]
        self.device_selection = ""
        self.rpc_stream = 0

    def signal_handler(self, sig, frame):
        """ Graceful shutdown.

        On Ctrl+C close the stream and disconnect from
        the RPC client.
        """

        print("Closing RPC stream...")
        self.rpc_stream.close()

        print("Closing Audiostream...")
        self.stream.stop_stream()
        self.stream.close()

        print("Stopping PyAudio...")
        self.p.terminate()
        sys.exit(0)

    def default_supported_device(self, device_set):
        """ Checks to see default device is supported.

        Searches to see if there is a device under 
        your default name that is supported by loopback.

        Args:
            api_info : finds what drivers the hardware
            is using, this is needed as loopback is
            only supported on WASAPI drivers.
        """
        for i in range(0, self.p.get_device_count()):
            api_info = self.p.get_host_api_info_by_index(self.p.get_device_info_by_index(i)["hostApi"])["name"]
            if(self.p.get_device_info_by_index(i)["name"] == self.p.get_default_output_device_info()["name"] and (api_info.find("WASAPI") != -1)):
                self.device_info = self.p.get_device_info_by_index(i)
                self.device_set = True

        return self.device_info, self.device_set
    
    def find_supported_devices(self, device_set):
        """ Finds supported devices and takes input
        
        If there were no default devices found that
        support loopback it will then ask the user
        to pick a device that does support it.

        If no devices support it, it will return
        and exit the application.

        Args:
            api_info : finds what drivers the hardware
            is using, this is needed as loopback is
            only supported on WASAPI drivers.

            valid_array : Adds index of devices that
            support loopback for user validation.

        Returns:
            device_info : If a device has been set
            succesfully the information will be saved
            to this variable. Otherwise it will return
            null.

            device_set : If a device has been set this
            will be changed to true to notify the script
            that this device has passed all validation
            and can be used for the audio stream.

        Raises:
            ValueError: If no valid input is selected
            it will output the error and loop around
            until inputs a correct selected device shown.
        """
        valid_array = []
        for i in range(0, self.p.get_device_count()):
            api_info = self.p.get_host_api_info_by_index(self.p.get_device_info_by_index(i)["hostApi"])["name"]
            if(api_info.find("WASAPI") != -1):
                valid_array.append(self.p.get_device_info_by_index(i)["index"])
                print (str(self.p.get_device_info_by_index(i)["index"]) + " : " + self.p.get_device_info_by_index(i)["name"])

        if(len(valid_array) < 1):
            return self.device_info, self.device_set

        print("\nYou are not connected to your default device or it doesn't support loopback. Luckily, these following devices do.\n")
        while not self.device_set:
            try:
                self.device_selection = int(input("Pick a device: "))
                if(self.device_selection in valid_array):
                    self.device_info = self.p.get_device_info_by_index(self.device_selection)
                    self.device_set = True
                else:
                    print("Please pick a number in the selection.")
            except ValueError:
                print("That is not a valid selection.")

        return self.device_info, self.device_set

    def no_devices_found(self):
        """ Failure output message.
         
        If there are no devices that can be used
        it will simply print out a message saying
        so and quit the application.
        """

        print("No devices that support this application were found, is WASAPI installed?")
        sys.exit()

    def open_stream(self, device_info, default_frames):
        """ Set the stream variables.
         
        Takes the inputs and sets all the variables
        for the stream.

        Args:
            channelcount : Checks the max input and
            output channels on the device and sets
            the stream variable so such.

        Returns:
            Returns the stream format.
        """
        # Open stream
        channelcount = self.device_info["maxInputChannels"] if (self.device_info["maxOutputChannels"] < self.device_info["maxInputChannels"]) else self.device_info["maxOutputChannels"]
        self.stream = self.p.open(
            format = pyaudio.paInt16,
            channels = channelcount,
            rate = int(self.device_info["defaultSampleRate"]),
            input = True,
            frames_per_buffer = self.default_frames,
            input_device_index = self.device_info["index"],
            as_loopback = True
        )
        return self.stream

    async def do(self, ip, port, protocol, stream, chunk):
        self.rpc_stream = await aiozmq.stream.create_zmq_stream(
            zmq_type=zmq.PUB, # pylint: disable=no-member
            bind=protocol+'://'+str(ip)+':'+str(port),
        )

        # Loop through reading the stream, 
        while True:
            # data = int(round(50*np.average(np.abs(np.frombuffer(stream.read(chunk),dtype=np.int16)))/2**16))
            data = int(round(audioop.rms(stream.read(chunk), 2)/1000))
            
            # Use Chr isn't the best. Best is to make a struct in the future.
            msg = [chr(data).encode()]
            self.rpc_stream.write(msg)

    def main(self): 
        signal.signal(signal.SIGINT, self.signal_handler)
        """ Sends volume over a socket.
        
        Loopsback the audio from the output device.
        reads the stream and gets a EMS value which
        is then sent over a RPC stream.
        """

        self.device_info, self.device_set = self.default_supported_device(self.device_set)

        if self.device_set == False:
            self.device_info, self.device_set = self.find_supported_devices(self.device_set)

        if self.device_set == False:
            self.no_devices_found()

        print("\nRPC Stream Information:\n")
        print("\t"+"RPC Stream State: Active")
        print("\t"+"Host IP Address: " +self.ip+":"+str(self.port))
        print("\t"+"Loopback Device: "+str(self.device_info["name"])+"\n")

        self.stream = self.open_stream(self.device_info, self.default_frames)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.do(self.ip, self.port, self.protocol, self.stream, self.chunk))

if __name__ == "__main__":
    with open("main.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    GetAudio().main()