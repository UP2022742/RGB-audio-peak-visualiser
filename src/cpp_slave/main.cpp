#include <iostream>
#include <cstddef>
#include <zmq.hpp>

int main(){
    // initialize the zmq context with a single IO thread
    zmq::context_t context{ 1 };
    std::string topicfilter = "A";

    // construct a REQ (request) socket and connect to interface
    zmq::socket_t socket{ context, ZMQ_SUB };
    socket.connect("tcp://192.168.1.106:5555");
    socket.setsockopt(ZMQ_SUBSCRIBE, topicfilter.c_str(), topicfilter.length());

    int counter = 0;
    for (;;){
        double f;
        zmq::message_t topic, message;

        // Try recieve messages if failure skip.
        try {
            socket.recv(topic, zmq::recv_flags::none);
            socket.recv(message, zmq::recv_flags::none);
            memcpy(&f, message.data(), sizeof(f));
            std::cout << f << std::endl;
        }
        catch (zmq::error_t& e) {
            std::cout << "W: interrupt received, proceeding…" << std::endl;
        }
    }
    return 0;
}