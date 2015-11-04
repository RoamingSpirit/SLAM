/*
** server.c -- a stream socket server demo
*/

#include "Server.h"

#include <iostream>

using namespace std;


int main(void)
{
    Server server;
    server.waitForClient();
}