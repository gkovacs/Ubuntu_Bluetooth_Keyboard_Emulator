#!/bin/bash

#Stop the background process
sudo /etc/init.d/bluetooth stop
sleep 1
while [ $(ps aux | grep bluetoothd | grep -v grep | wc -l) -ne 0 ]; do
    echo "killall bluetoothd"
    sudo killall bluetoothd
    sleep 1
done
# Turn on Bluetooth
#sudo hciconfig hcio up
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
    tmux send-keys -t BT-HID:os.0 'cd $C_PATH && sudo /usr/sbin/bluetoothd --compat --nodetach --debug -p time ' C-m
    tmux send-keys -t BT-HID:os.1 'cd $C_PATH/server && sleep 1 && sudo python btk_server.py ' C-m
    tmux send-keys -t BT-HID:os.2 'cd $C_PATH && sleep 1 && sudo /usr/bin/bluetoothctl' C-m
    tmux send-keys -t BT-HID:os.3 'cd $C_PATH/keyboard/ && sleep 5 && sudo python kb_client.py' C-m
    tmux set-option -t BT-HID mouse on
fi
