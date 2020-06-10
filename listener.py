# coding: utf-8
import asyncio
import aiozmq
import zmq
import yaml

with open("listener.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

protocol = cfg["RPC"]["protocol"]
IP = cfg["RPC"]["IP"]
port = cfg["RPC"]["port"]

async def do():
    stream = await aiozmq.stream.create_zmq_stream(
        zmq_type=zmq.SUB, # pylint: disable=no-member
        connect=protocol+'://'+str(IP)+':'+str(port),
    )
    stream.transport.subscribe(b'')

    while True:
        msg = await stream.read()
        print(ord(msg[0]))

loop = asyncio.get_event_loop()
loop.run_until_complete(do())