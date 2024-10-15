# Dashboard for Electrical Motorcycles
<p align="center">
  <img src="https://github.com/user-attachments/assets/c8a2d370-616b-4791-8a00-bfb4a25b40b3" />
</p>

For the **Motorsport Competition** there was the need, of course, of a dashboard for the **electrical motorcycle**.
This dashboard created with **Kivy** to display and manage info coming from the CAN bus and the picture above is the one that was displayed on the **Raspberry-PI's screen**.

## How to setup VIRTUAL CAN to test the dashboard on your local system:
We were testing the BMS aswell during the creation of the dashboard so the code to **manage the CAN bus** came in handy for this other project.
We indeed need to setup the **VCAN** on the raspberry so that we can **emulate the "receiving" datas** coming from the BMS, run the following commands:
```
sudo apt-get install can-utils
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0            
cansend can0 18#0102030405060708
```
The last command lets you test both the **can0 interface**and the **can package**

## How to run the code:
Inside the **'PROJECT'/DASH/** folder, run the following command:
```
sudo python3 ./main.py
```
