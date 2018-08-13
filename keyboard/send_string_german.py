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
import keylayout_german

mods = {
"R_GUI"		: 0,
"R_ALT"		: 1,
"R_Shift"     : 2,
"R_Control"   : 3,
"L_GUI"       : 4,
"L_ALT"       : 5,
"L_Shift"     : 6,
"L_Control"   : 7
}

class BtkStringClient():

        """simple client of the Bluetooth Keyboard Emulator
        writes a string (containing only printable/typable symbols for German) to the BTK Keyboard assuming selected GERMAN keyboard layout at the target (paired bluetooth device / BT HID host role)
        """

        #constants
    	KEY_DOWN_TIME=0.04
    	KEY_DELAY=0.08




        def __init__(self,chartable):
            self.chartable=chartable

            #the structure for a bt keyboard input report (size is 10 bytes)

            self.state=[
                    0xA1, #this is an input report
                    0x01, #Usage report = Keyboard
                    #Bit array for Modifier keys
                    [0, #Right GUI - Windows Key
                     0, #Right ALT
                     0, #Right Shift
                     0, #Right Control
                     0, #Left GUI
                     0, #Left ALT
                     0, #Left Shift
                     0],    #Left Control
                    0x00,   #Vendor reserved
                    0x00,   #rest is space for 6 keys
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00]


	    self.scancodes={
		" " : "KEY_SPACE",
        "\t": "KEY_TAB",
        "\n": "KEY_ENTER"
	     }


            #connect with the Bluetooth keyboard server
            print "setting up DBus Client"

            self.bus = dbus.SystemBus()
            self.btkservice = self.bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
            self.iface = dbus.Interface(self.btkservice,'org.yaptb.btkbservice')




        def send_key_state(self):

            """sends a single frame of the current keys state to the emulator server"""

            bin_str=""
            element=self.state[2]
            for bit in element:
                    bin_str += str(bit)
            self.iface.send_keys(int(bin_str,2),self.state[4:10]  )


        def send_key_down(self, scancode):

            """sends a down event to the server for a single key (including modifiers as set manually)"""

            self.state[4]=scancode
            self.state[5:10]=[0]*5 #unset all other potentially pressed keys
            self.send_key_state()


        def send_key_up(self):

            """sends (all) key(s) up event to the server (not changing modifier keys)"""

            self.state[4:10]=[0]*6
            self.send_key_state()

        def send_keystroke(self,scancode):

            """sends a keystroke to the server"""

            self.send_key_down(scancode)
            time.sleep( BtkStringClient.KEY_DOWN_TIME)
            self.send_key_up()
            time.sleep( BtkStringClient.KEY_DELAY)


        def send_key_test(self):

            """send euro sign"""
            self.state[2][mods["R_ALT"]]=1
            self.send_keystroke(8)

        def send_multiple_key_test(self):

            """multiple keys per report test"""
            self.state[2][mods["L_Shift"]]=1
            self.state[4]=4
            self.state[5]=5
            self.state[6]=6
            self.state[7]=7
            self.state[8]=8
            self.state[9]=9
            self.send_key_state()
            time.sleep(0.1)
            self.state[2][mods["L_Shift"]]=0
            self.state[4]=10
            self.state[5]=11
            self.state[6]=12
            self.state[7]=13
            self.state[8]=14
            self.state[9]=15
            self.send_key_state()
            time.sleep(0.1)
            self.state[4]=8 ### pressing the same key in the same report won't work
            self.state[5]=0
            self.state[6]=8
            self.state[7]=9
            self.state[8]=9
            self.state[9]=0
            self.send_key_state()
            time.sleep(0.1)
            self.send_key_up()
            print "yeah"

        def send_string(self, string_to_send):
            #string_to_send = unicode(string_to_send,"utf-8")
            print "Sending " + string_to_send
            # string_to_send = unicode(sys.argv[1],"unicode-escape")

            for c in string_to_send: # split into chars

                events = self.chartable[c]
                for e in events: # send key stroke(s) for one char
                    for modifier in e[0]:
                        self.state[2][mods[modifier]]=1 # set modifier(s)
                    self.send_keystroke(e[1])   # set and send keycode
                    self.state[2]=[0,0,0,0,0,0,0,0] # reset modifier keys






if __name__ == "__main__":


    if(len(sys.argv) <2):
        print "missing parameter: \nUsage: send_string <string to send>"
        print "sending test string... you can use this to verify correctness of your GERMAN keyboard layout on the target device. compare sent string and displayed string"
        dc = BtkStringClient(keylayout_german.chartable)
        string_to_send = u" ^@1234567890ß´@qwertzuiopü+#asdfghjklöäyxcvbnm,.-<!\"§$%&/()=?QWERTZUIOPÜ*'ASDFGHJKLÖÄYXCVBNM;:_>²³{[]}\\@€~µ|âêîôûÂÊÎÔÛ^áéíóúýÁÉÍÓÚÝ´àèìòùÀÈÌÒÙ`"
        dc.send_string(string_to_send)
        #dc.send_multiple_key_test()
        #dc.send_key_test()
        exit()

    # One-character Unicode strings can also be created with the unichr() built-in function, which takes integers and returns a Unicode string of length 1 that contains the corresponding code point.
    # The reverse operation is the built-in ord() function that takes a one-character Unicode string and returns the code point value:

    string_to_send = unicode(sys.argv[1],"utf-8")
    print "Setting up virtual Bluetooth keyboard emulator client"
    dc = BtkStringClient(keylayout_german.chartable)
    dc.send_string(string_to_send)
    print " ====> Done."
