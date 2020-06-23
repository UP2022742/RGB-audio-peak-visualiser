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

void startSubscriber()
{
    zmq::context_t zmq_context(1);
    zmq::socket_t zmq_socket(zmq_context, ZMQ_SUB);
    zmq_socket.connect("tcp://192.168.1.117:5555");

    zmq::socket_t killer_socket(zmq_context, ZMQ_PAIR); // This socket is used to terminate the loop on a signal
    killer_socket.bind("tcp://192.168.1.117:5555");

    zmq_socket.setsockopt(ZMQ_SUBSCRIBE, TOPIC.c_str(), TOPIC.length()); // Subscribe to any topic you want here
    zmq::pollitem_t items [] = {
        { zmq_socket, 0, ZMQ_POLLIN, 0 },
        { killer_socket, 0, ZMQ_POLLIN, 0 }
    };
    while(true)
    {
        int rc = 0;
        zmq::message_t topic;
        zmq::message_t msg;
        zmq::poll (&items [0], 2, -1);

        if (items [0].revents & ZMQ_POLLIN)
        {
            std::cout << "waiting on recv..." << std::endl;
            rc = zmq_socket.recv(&topic, ZMQ_RCVMORE);  // Works fine
            rc = zmq_socket.recv(&msg) && rc;
            if(rc > 0) // Do no print trace when recv return from timeout
            {
                std::cout << "topic:\"" << std::string(static_cast<char*>(topic.data()), topic.size()) << "\"" << std::endl;
                std::cout << "msg:\"" << std::string(static_cast<char*>(msg.data()), msg.size()) << "\"" << std::endl;
            }
        }
        else if (items [1].revents & ZMQ_POLLIN)
        {
            if(s_interrupted == 1)
            {
                std::cout << "break" << std::endl;
                break;
            }
        }
    }
}

int main() {
    bool run = true;
    std::thread t_sub(startSubscriber);