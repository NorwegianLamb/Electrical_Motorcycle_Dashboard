# Dashboard for Electrical Motorcycles
Dashboard created with Kivy to display and manage info coming from the CAN bus

## How to setup VIRTUAL CAN to test the dashboard on your local system:
Run the following commands:
```
sudo apt-get install can-utils
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0            
cansend can0 18#0102030405060708
```
The last command lets you test both the can0 interface and the can package

## How to run the code:
Inside the <PROJECT>/DASH/ folder, run the following command:
```
sudo python3 ./main.py
```
