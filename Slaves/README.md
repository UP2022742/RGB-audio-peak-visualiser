<h1>Arduino</h1>
<p>The arduino example is preferred as it's much more effecient on performance, power consumption and additioanlly more functionality.</p>
<p>In order to get it working with the Arduino you will first need the Arduino IDE</p>
<p>https://www.arduino.cc/en/main/software</p>
<p>After you have installed which for your desired platform open the file in the IDE and flash the Arudino with the arrow pointing right at the top of the IDE.</p>
<h1>Raspberry Pi</h1>
<p>The raspberry pi is not the reccomended option as it's function is limited and much less efficient for the code than the arduino but if it's for a simple hands on project it works absolutely fine.</p>
<p>In order to get this setup, flash the Raspberry Pi with the latest version of Raspbian Server, or Raspbian Lite as it's called on the website. The link for which can be found here.</p>
<p>https://www.raspberrypi.org/downloads/raspberry-pi-os/</p>
<p>After that is done and you are successfully booted into the operating system, then copy all the files over to the Raspberry Pi, either through SCP or whatever crazy method you wish to do. Make sure that Raspbian has Python3 installed, unlike the host file a specific version of Python3 isn't required here. Make sure that the Raspberry Pi is connected to the Local Area Network (LAN) and check that the IP address and port is the same as the host in which you're running this off by opening up the listener.yaml file and changing the values accordingly. Run install the dependencies through the command:</p>
<p>sudo pip install -r requirements.txt</p>
<p>After all depdendencies are installed you should be ready to run the python file in which you wish to start with. Open one of the scripts with the command with rabbit.py being the example.</p>
<p>sudo python3 rabbit.py</p>
