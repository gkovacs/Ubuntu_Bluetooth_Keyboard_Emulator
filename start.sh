#!/bin/bash

#Stop the background process
sudo /etc/init.d/bluetooth stop
# Turn on Bluetooth
sudo hciconfig hcio up
# Update  mac address
./updateMac.sh
#Update Name
./updateName.sh BT_Keyboard
#Get current Path
export C_PATH=$(pwd)
#Create Tmux session
tmux has-session -t  BT-HID
if [ $? != 0 ]; then

    sudo --validate
    tmux new-session -s BT-HID -n os -d
    tmux split-window -h -t BT-HID
    tmux split-window -v -t BT-HID:os.0
    tmux split-window -v -t BT-HID:os.1
    tmux send-keys -t BT-HID:os.0 'cd $C_PATH && sudo /usr/sbin/bluetoothd --nodetach --debug -p time ' C-m
    tmux send-keys -t BT-HID:os.1 'cd $C_PATH/server && sudo python btk_server.py ' C-m
    tmux send-keys -t BT-HID:os.2 'cd $C_PATH && sudo /usr/bin/bluetoothctl' C-m
    tmux send-keys -t BT-HID:os.3 'cd $C_PATH/keyboard/ && sleep 5 && sudo python kb_client.py' C-m
    tmux set-option -t BT-HID mouse on
fi
