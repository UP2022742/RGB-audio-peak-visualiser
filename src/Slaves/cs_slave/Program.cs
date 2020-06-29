using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NetMQ;
using NetMQ.Sockets;
namespace SubscriberA
{
    class Program
    {
        static void Main(string[] args)
        {
            string uuid = "A";
            using (var subSocket = new SubscriberSocket())
            {
                subSocket.Connect("tcp://192.168.1.106:5555");
                // subSocket.Options.ReceiveHighWatermark = 0;
                subSocket.Subscribe(uuid);
                Console.WriteLine("Subscriber socket connecting...");
                while (true)
                {
                    string uuid_value = subSocket.ReceiveFrameString();
                    byte[] RMSValue = subSocket.ReceiveFrameBytes();
                    string result = string.Concat(Enumerable.Repeat("#", (int)(Math.Round((BitConverter.ToDouble(RMSValue, 0)*200)))));
                    Console.WriteLine(result);
                }
            }
        }
    }
}