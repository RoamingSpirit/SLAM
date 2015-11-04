/* 
 * File:   Server.h
 * Author: Nils
 *
 * Created on 3. November 2015, 16:18
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>

#include <string>

#include "Reader.h"

#define PORT "3490"  // the port users will be connecting to

#define BACKLOG 10     // how many pending connections queue will hold

#ifndef SERVER_H
#define	SERVER_H


class Server {
public:
    Server();
    virtual ~Server();
    
    void waitForClient();
private:
    //Reader reader;
    int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage their_addr; // connector's address information
    socklen_t sin_size;
    struct sigaction sa;
    int yes;
    char s[INET6_ADDRSTRLEN];
    int rv;
    
    void setup();
    void sendData();
    
};

#endif	/* SERVER_H */

