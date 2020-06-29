#include <string>
#include <iostream>
#include <zmq.hpp>
#include <Windows.h>
#include <signal.h>

inline static int s_sendmore(void* socket, const char* string) {
    int rc;
    zmq_msg_t message;
    zmq_msg_init_size(&message, strlen(string));
    memcpy(zmq_msg_data(&message), string, strlen(string));
    rc = zmq_msg_send(&message, socket, ZMQ_SNDMORE);
    assert(-1 != rc);
    zmq_msg_close(&message);
    return (rc);
}

inline static int s_send(void* socket, const char* string, int flags = 0) {
    int rc;
    zmq_msg_t message;
    zmq_msg_init_size(&message, strlen(string));
    memcpy(zmq_msg_data(&message), string, strlen(string));
    rc = zmq_msg_send(&message, socket, flags);
    assert(-1 != rc);
    zmq_msg_close(&message);
    return (rc);
}

int main(){

    // Start socket.
    using namespace std::chrono_literals;
    zmq::context_t context{ 1 };
    zmq::socket_t socket{ context, ZMQ_PUB };

    // IP to bind to.
    socket.bind("tcp://192.168.1.106:5555");

    // Write the topic and the writing value.
    const char* topic = "A";
    const char* message = "What does this do?";

    // Loop sending over the socket.
    for (;;){
        try {
            s_sendmore(socket, topic);
            s_send(socket, message);
        }
        catch (zmq::error_t& e) {
            std::cout << "W: interrupt received, proceeding…" << std::endl;
        }
        Sleep(1);
    }
    return 0;
}
