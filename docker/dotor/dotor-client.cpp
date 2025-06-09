#include <stdio.h>
#include <sys/socket.h>
#include <iostream>
#include <netinet/in.h>
#include <string>
#include <stdio.h>
//#include <cstring>
//#include <arpa/inet.h>
//#include <unistd.h>

//Abandoned dude to time-constraints, used python instead

int main(){

    //Set up listening
    int dnsSocket = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(1337);
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    bind(dnsSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress));

    //Print message, debug:
    listen(dnsSocket, 5);
    int socketInput = accept(dnsSocket, nullptr, nullptr);
    char buffer[1024] = {0};
    recv(dnsSocket, buffer, sizeof(buffer), 0);
    std::cout << "Message from client: " << buffer << "end"<< std::endl;
    shutdown(dnsSocket,0);

}