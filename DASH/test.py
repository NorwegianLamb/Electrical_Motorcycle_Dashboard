from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
#import RPi.GPIO as GPIO
import threading
import time
import can
import os
import keyboard

# ------------------------------------------------------------------------------#

# ------------------------------------------------------------------------------#

# Bring up can0 vcan0 slcan0 interface
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
time.sleep(1)

bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate='250000')  # bus channel & type refer to python-can docs

class ScreenRace(Screen):
    pass


class ScreenRace2(Screen):
    pass


class ScreenRace3(Screen):
    pass


class ScreenBox(Screen):
    pass


ceck_State = 0
button1 = False
button2 = False
buttonb = False

class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)

    # Cambia il valore degli if per cambiare la schermata
    def update(self, dt):
        global ceck_State, button1, button2, buttonb
        if(buttonb):
            print("funziona")
            self.transition.direction = 'up'
            self.current = 'screenbox'
            ceck_State = 10
            buttonb = False
        elif(button1):
            print("funziona1")
            self.transition.direction = 'left'
            self.current = 'screenrace'
            ceck_State = 1
            button1 = False
        elif(button2):
            print("funziona2")
            self.transition.direction = 'left'
            self.current = 'screenrace2'
            ceck_State = 2
            button2 = False
        else:
            pass
        # ------------------------------------------
        if keyboard.is_pressed('b'):
            self.transition.direction = 'up'
            self.current = 'screenbox'
            ceck_State = 10
        elif keyboard.is_pressed('1'):
            self.transition.direction = 'left'
            self.current = 'screenrace'
            ceck_State = 1
        elif keyboard.is_pressed('2'):
            self.transition.direction = 'left'
            self.current = 'screenrace2'
            ceck_State = 2
        elif keyboard.is_pressed('3'):
            self.transition.direction = 'left'
            self.current = 'screenrace3'
            ceck_State = 3
        else:
            pass


class CanThread(threading.Thread):
    def run(self):
        ceck_fault = False
        start = time.time()
        counter = 2
        time_Flag = False
        self.app = App.get_running_app()
        try:
            while True:
                # ADD LOOP to understand if "elif"s add TIME COMPLEXITY (counter + print for every ID) -> check missing counters in messages
                    # IF SO:
                        # -> ADD PRIORITIES clocks (r.up old days)
                        # -> manage bus load and set priority from analyzer
                message = bus.recv()
                global button1, button2, buttonb
                if message.arbitration_id == 0x218: # what if "ALL_FALSE" state? switch states to be true with prio and all FALSE to that?
                    if(message.data[4] == 0x01):
                        button1 = True
                    elif(message.data[4] == 0x02):
                        button2 = True
                    elif(message.data[4] == 0x03):
                        buttonb = True
                    else:
                        pass
                elif message.arbitration_id == 0x700:  # TDPO 1
                    self.app.fault = 256 * message.data[0] + message.data[1]
                    self.app.V_BAT_HV = 256 * message.data[2] + message.data[3]
                    self.app.A_BAT_HV = 256 * message.data[4] + message.data[5]
                    self.app.T_INV = message.data[6]
                elif message.arbitration_id == 0x701:  # TDPO 2
                    self.app.VEL_RPM = 256 * 256 * 256 * message.data[0] + 256 * 256 * message.data[1] + 256 * \
                                       message.data[2] + message.data[3]
                    self.app.TRAC_DRIVE_S = message.data[4]
                    self.app.T_MOT = 256 * message.data[5] + message.data[6]
                elif message.arbitration_id == 0x702:  # TDPO 3
                    self.app.TARGET_Id = 256 * message.data[0] + message.data[1]
                    self.app.TARGET_Iq = 256 * message.data[2] + message.data[3]
                    self.app.Id = 256 * message.data[4] + message.data[5]
                    self.app.Iq = 256 * message.data[6] + message.data[7]
                elif message.arbitration_id == 0x703:  # TDPO 4
                    self.app.TQ_DEMAND = 256 * message.data[0] + message.data[1]
                    self.app.TQ_VALUE = 256 * message.data[2] + message.data[3]
                    self.app.V_MOD = 256 * message.data[4] + message.data[5]
                    self.app.INDUCTANCE_MEAS = 256 * message.data[6] + message.data[7]
                elif message.arbitration_id == 0x704:  # TDPO 5
                    self.app.Ud = 256 * message.data[0] + message.data[1]
                    self.app.Uq = 256 * message.data[2] + message.data[3]
                    self.app.MONO = 256 * message.data[5] + message.data[4]
                    self.app.BRAKE = 256 * message.data[6] + message.data[7]
                elif message.arbitration_id == 0x800:  # LAP 1
                    self.app.LAP_TIME = 256 * 256 * 256 * message.data[0] + 256 * 256 * message.data[1] + 256 * \
                                       message.data[2] + message.data[3]
                    self.app.LAP_BEST = 256 * 256 * 256 * message.data[4] + 256 * 256 * message.data[5] + 256 * \
                                       message.data[6] + message.data[7]
                elif message.arbitration_id == 0x801:  # LAP 2
                    self.app.n_LAP = 256 * message.data[0] + message.data[1]
                    self.app.PARTIAL_TIME = 256 * 256 * 256 * message.data[2] + 256 * 256 * message.data[3] + 256 * \
                                       message.data[4] + message.data[5]
                    self.app.n_SAT = 256 * message.data[6] + message.data[7]
                elif message.arbitration_id == 0x900:  # GPS 1
                    self.app.Speed_km_h = 256 * message.data[0] + message.data[1]
                    self.app.ALTITUDE = 256 * 256 * 256 * message.data[2] + 256 * 256 * message.data[3] + 256 * \
                                       message.data[4] + message.data[5]
                    self.app.Speed_m_s = 256 * message.data[6] + message.data[7]
                elif message.arbitration_id == 0x901:  # GPS 2
                    self.app.LATITUDE = 256 * 256 * 256 * message.data[0] + 256 * 256 * message.data[1] + 256 * \
                                       message.data[2] + message.data[3]
                    self.app.LONGITUDE = 256 * 256 * 256 * message.data[4] + 256 * 256 * message.data[5] + 256 * \
                                       message.data[6] + message.data[7]
                elif message.arbitration_id == 0x1000:  # DATALOGGER
                    self.app.V_BAT_LV = 256 * message.data[0] + message.data[1]
                    self.app.ODO = 256 * message.data[2] + message.data[3]
                    self.app.T_WAT = 256 * message.data[2] + message.data[3]
                    self.app.FRONT = 256 * message.data[2] + message.data[3]
                if ceck_State == 3:
                    delta = time.time() - start
                    if delta > 0.250:
                        time_Flag = not time_Flag
                        self.app.shiftRpm = time_Flag * 180
                        start = time.time()
                if keyboard.is_pressed('f'):
                    self.app.fault = 1
                else:
                    self.app.fault = 0
                if (self.app.n_SAT > 1) or keyboard.is_pressed('s'):
                    self.app.s_SAT = 1
                else:
                    self.app.s_SAT = 0
                self.app.time_now = time.strftime("%H:%M", time.localtime())
        except KeyboardInterrupt:
            os.system("sudo /sbin/ip link set can0 down")
            print('\n\rKeyboard interrtupt')


class DashApp(App):

    # ---Inverter---
    fault = NumericProperty(0)  # NumericProperty(0)
    # ---HV BATTERY
    V_BAT_HV = NumericProperty(0)  # NumericProperty(0)
    A_BAT_HV = NumericProperty(0)
    T_INV = NumericProperty(0)  # NumericProperty(0)
    # ---MOTOR
    VEL_RPM = NumericProperty(0)
    TRAC_DRIVE_S = NumericProperty(0)
    T_MOT = NumericProperty(0)  # NumericProperty(0)
    T_WAT = NumericProperty(0)
    # ---Id Iq
    TARGET_Id = NumericProperty(0)
    TARGET_Iq = NumericProperty(0)
    Id = NumericProperty(0)
    Iq = NumericProperty(0)
    # ---TORQUE
    TQ_DEMAND = NumericProperty(0)
    TQ_VALUE = NumericProperty(0)
    # ---V MODULATION
    V_MOD = NumericProperty(0)
    # ---INDUCTANCE MEASURED
    INDUCTANCE_MEAS = NumericProperty(0)
    # ---Ud Uq
    Ud = NumericProperty(0)
    Uq = NumericProperty(0)
    # ---TIME
    LAP_TIME = StringProperty(' ')
    LAP_BEST = StringProperty(' ')
    n_LAP = NumericProperty(0)
    PARTIAL_TIME = NumericProperty(0)  # +-BEST
    # ---GPS DATA
    n_SAT = NumericProperty(0)
    Speed_km_h = NumericProperty(0)
    ALTITUDE = NumericProperty(0)
    Speed_m_s = NumericProperty(0)
    LATITUDE = NumericProperty(0)
    LONGITUDE = NumericProperty(0)
    # ---DATALOGGER
    V_BAT_LV = NumericProperty(0)  # NumericProperty(0)
    ODO = NumericProperty(0)
    # ---DINAMICA
    FRONT = NumericProperty(0)
    MONO = NumericProperty(0)
    BRAKE = NumericProperty(0)
    #---VARIABILI UTILI
    s_SAT = NumericProperty(0)
    SOC = NumericProperty(0)
    time_now = NumericProperty(0)
    start_program = 0
    H = 0
    shiftRpm = NumericProperty(0)
    

    txtLAB = NumericProperty(18)
    txtNUM = NumericProperty(65)

    def build(self):
        self.title = "Dashboard Electric"
        Window.size = (800, 480)
        Window.clearcolor = (0.07, 0.05, 0.18, 1)
        thread1 = CanThread()
        thread1.start()
        sm = Manager(transition=SlideTransition())
        Clock.schedule_interval(sm.update, 0.01)

        return sm


if __name__ == '__main__':
    DashApp().run()
