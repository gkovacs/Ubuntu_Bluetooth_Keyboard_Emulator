#!/usr/bin/python
# -*- coding: utf-8 -*-

import os #used to all external commands
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import thread
import keymap
from send_string_german import BtkStringClient
import keylayout_en_us


if __name__ == "__main__":


    if(len(sys.argv) <2):
        print "missing parameter: \nUsage: send_string <string to send>"
        print "sending test string... you can use this to verify correctness of your AMERICAN English keyboard layout on the target device. compare sent string and displayed string"
        dc = BtkStringClient(keylayout_en_us.chartable)
        string_to_send = u" `1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"
        dc.send_string(string_to_send)
        #dc.send_multiple_key_test()
        #dc.send_key_test()
        exit()

    # One-character Unicode strings can also be created with the unichr() built-in function, which takes integers and returns a Unicode string of length 1 that contains the corresponding code point.
    # The reverse operation is the built-in ord() function that takes a one-character Unicode string and returns the code point value:

    string_to_send = unicode(sys.argv[1],"utf-8")
    print "Setting up virtual Bluetooth keyboard emulator client"
    dc = BtkStringClient(keylayout_en_us.chartable)
    dc.send_string(string_to_send)
    print " ====> Done."
