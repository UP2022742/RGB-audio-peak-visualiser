using System;
using System.Threading;
using NetMQ;
using NetMQ.Sockets;
using NAudio.CoreAudioApi;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Publisher
{
    class Program
    {
        static (int, string, string, string) ret_varaibles(){
            using(var sr = new StreamReader("config.json")){
                var jObject = JObject.Load(new JsonTextReader(sr));

                // Find the way of getting a value as a int and remove this useless line.
                var Delay = Int32.Parse(jObject.GetValue("DELAY").Value<string>());
                var IP = jObject.GetValue("IP").Value<string>();
                var PORT = jObject.GetValue("PORT").Value<string>();
                var PROTOCOL = jObject.GetValue("PROTOCOL").Value<string>();
                return (Delay, IP, PORT, PROTOCOL);
            }
        }

        static void new_thread(string new_command, byte[] volume , PublisherSocket pubSocket){
            pubSocket.SendMoreFrame(new_command).SendFrame(volume);
        }
        static void Main(string[] args)
        {
            var values = ret_varaibles();
            int DELAY = values.Item1;
            string IP = values.Item2;
            string PORT = values.Item3;
            string PROTOCOL = values.Item4;

            Console.WriteLine("\nRPC Stream Information:\n");
            Console.WriteLine("\tRPC Stream State: Active");
            Console.WriteLine("\tHost IP Address: " + PROTOCOL + "://" + IP + ":" + PORT);
            Console.WriteLine("\tDelay: " + DELAY + "ms\n");

            using (var pubSocket = new PublisherSocket())
            {
                MMDeviceEnumerator enumerator = new MMDeviceEnumerator();
                MMDevice defaultDevice = enumerator.GetDefaultAudioEndpoint(DataFlow.Render, Role.Console);
                // pubSocket.Options.SendHighWatermark = 0;
                pubSocket.Bind(PROTOCOL + "://"+ IP +":"+ PORT);

                string new_command = "B";
                while(true){
                    double result = defaultDevice.AudioMeterInformation.MasterPeakValue;
                    byte[] volume = BitConverter.GetBytes(result);
                    new_thread(new_command, volume, pubSocket);
                    Thread.Sleep(DELAY);
                }
            }

        }
    }
}