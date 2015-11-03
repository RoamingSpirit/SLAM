#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Lukas"
__date__ = "$03.11.2015 17:05:00$"

from simplereceiver import SimpleReceiver
if __name__ == "__main__":
    print "Initialize socket.."
    rec=SimpleReceiver()
    rec.connect()
    rec.listen()
