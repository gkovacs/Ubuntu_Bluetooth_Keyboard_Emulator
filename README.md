
# Ubuntu Bluetooth HID keyboard Emulation / Mirroring

Emulates a Bluetooth HID keyboard by mirroring / sharing keystrokes from an attached (or internal) keyboard on a Ubuntu device or sending (multiple) virtual key events
via a python script

### requirements:

- Ubuntu (16.04) device with working Bluetooth BlueZ stack
- python 2.7 with Pybluez, evdev module


##### test configuration:
Ubuntu 16.04 (4.4.0-24-generic kernel) amd64 - BlueZ 5.37
Python 2.7.12 (PyBluez 0.22, evdev 0.7)
Intel® Centrino® Advanced-N 6235, Dualband  bluetooth chipset
Sony D5803 Android 6 smartphone (bluetooth HID v1.1 host role)

## Step 1: Install requirements and configure setup
- run `sudo ./setup.sh`
- if the keyboard you want to use is not `/dev/input/event4` change `self.dev = InputDevice("/dev/input/event4")` in the *keyboard/kb_client.py* file. You can determine what your keyboard is by running the command `sudo evtest`
- if you want to deploy this tool on multiple devices you should change the advertised bluetooth name in the startup script

## Step 2: Run
- `sudo ./start.sh`  runs necessary steps to expose your keyboard as Bluetooth HID device
- `sudo tmux a` opens up the "command center"
- now connect and pair your BT_Keyb on your target device (e.g. Android device)

## Step 3: Pause sharing keyboard
- by clicking in the right lower corner and pushing `CTRL-C` while your keyboard is mirrored you can interrupt mirroring the Keyboard
- by rerunning `sudo python kb_client.py` you start sharing your keyboard again

 NOTE: Every key you press will usually trigger an action on both devices!!! So be careful in what you are typing! Best seems if you open a text editor and type there. The reason for reading from the raw event file is that it allows to catch alt-tab key combination and media keys (play, next track, etc.) in an easy way. Feel free to extend this tool by an additional keyboard-client and create a pull request if you know how to write a special window which will forward all keyboard events only to the bluetooth server as long as it is focussed (without loosing focus on alt-tab events).

## Step 4: Terminate the tool
  go to the "command center" window and push` CTRL-b` followed by `&` and `y`
  (simply closing the console won't terminate the tool!)

# Disclaimer:
This tool is a slightly modified version of https://github.com/quangthanh010290/BL_keyboard_RPI in order to work for ubuntu. See this tutorial http://www.mlabviet.com/2017/09/make-raspberry-pi3-as-emulator.html as well as this [video demo](https://www.youtube.com/watch?v=fFpIvjS4AXs) for a step by step installation guide.

# Troubleshooting

## Bluetooth server

```
sudo /etc/init.d/bluetooth stop
sudo killall bluetoothd
sudo /usr/sbin/bluetoothd --nodetach --debug -p time
```

## Pairing

Note that for the pairing process, you may need to do the following:

    sudo /usr/bin/bluetoothctl

```
> agent on
> default-agent
> scan on
> discoverable on
```

