#include <thread>
#include <zmq.hpp>
#include <iostream>
#include <signal.h>
#include <io.h>
#include <windows.h>


static int s_interrupted = 0;
static void s_signal_handler (int signal_value)
{
    if(s_interrupted == 0)
    {
        std::cout << "sighandler" << std::endl;
        s_interrupted = 1;

        zmq::context_t context(1);
        zmq::socket_t socket(context, ZMQ_PAIR);
        socket.connect("tcp://192.168.1.117:5555");
        zmq::message_t msg;
        memcpy(msg.data(),"0", 1);
        socket.send(msg);
    }
}

const std::string TOPIC = "4567";

void startPublisher()
{
    zmq::context_t zmq_context(1);
    zmq::socket_t zmq_socket(zmq_context, ZMQ_PUB);
    zmq_socket.bind("tcp://192.168.1.117:5555");
    Sleep(10000);
    zmq::message_t msg(3);
    zmq::message_t topic(4);
    for(int i = 0; i < 10; i++) {
        memcpy(topic.data(), TOPIC.data(), TOPIC.size()); // <= Change your topic message here
        memcpy(msg.data(), "abc", 3);
        try {
            zmq_socket.send(topic, ZMQ_SNDMORE); 
            zmq_socket.send(msg); 
        } catch(zmq::error_t &e) {
            std::cout << e.what() << std::endl;
        }
        msg.rebuild(3);
        topic.rebuild(4);
        Sleep(1); // Temporisation between message; not necessary
    }
}

int main() {
    bool run = true;
    Sleep(1); // Slow joiner in ZMQ PUB/SUB pattern
    std::thread t_pub(startPublisher);
    t_pub.join();