"""
Author: Flavio Gjoni
Description: Dashboard for motorvehicles (manage CAN to implement)
Version: 1.02x
"""
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty, ColorProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.lang import Builder
from datetime import datetime
from datetime import timedelta
import threading
import time
import keyboard
import platform
import can

# PRE-CONF --------------------------------------------------------------------------

is_raspberry_pi = platform.machine() == '???'
# bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate='250000')
check_State = 0
button1 = False
button2 = False
buttonb = False
def toggle_relay():
    relay.toggle()
if is_raspberry_pi:
    from gpiozero import LED, Button
    gpio_pin = 17
    relay = LED(gpio_pin)
    button = Button(gpio_pin)
    button.when_pressed_screen_sport = toggle_relay
resource_add_path('./images')
resource_add_path('./fonts')

# RACE SCREENS ----------------------------------------------------------------------
class ScreenRace(Screen):
    pass

class ScreenRace2(Screen):
    pass

class ScreenBox(Screen):
    pass
# ------------------------------------------------------------------------------------


class Manager(ScreenManager):
    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)

    # Changing screen page based on BUTTON_STATE
    """
    def update(self, dt):
        global check_State
        global button1, button2, buttonb
        if buttonb:
            self.transition.direction = 'up'
            self.current = 'screenbox'
            check_State = 10
            buttonb = False
        elif button1:
            self.transition.direction = 'left'
            self.current = 'screenrace'
            check_State = 1
            button1 = False
        elif button2:
            self.transition.direction = 'left'
            self.current = 'screenrace2'
            check_State = 2
            button2 = False
        else:
            pass
    """
    def update(self, dt):
        global ceck_State
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
        else:
            pass

class CanThread(threading.Thread):
    def run(self):
        check_fault = False
        start = time.time()
        counter = 2
        time_Flag = False

        self.app = App.get_running_app()
        self.app.n_SAT = 5
        self.app.T_WAT = 56

        t = 1
        try:
            while 1:
                message = bus.recv()
                global button1, button2, buttonb
                if message.arbitration_id == 0x317: # BUTTON 1
                    button1 = True
                elif message.arbitration_id == 0x318: # BUTTON 2
                    button2 = True
                elif message.arbitration_id == 0x335: # BUTTON 1
                    button1 = True
                elif message.arbitration_id == 0x336: # BUTTON 2
                    button2 = True
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
                    self.app.MONO = 256 * message.data[4] + message.data[5]
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
                if check_State == 3:
                    delta = time.time() - start
                    if delta > 0.250:
                        time_Flag = not time_Flag
                        self.app.shiftRpm = time_Flag * 180
                        start = time.time()
                else:
                    counter = counter + 1
                    if counter == 100:
                        counter = 0
                        check_fault = not check_fault


                self.app.shiftRpm = counter
                # Fault test
                #if check_fault == True:
                self.app.LAP_TIME = str('1:02.580')

                if keyboard.is_pressed('f'):
                    self.app.fault = 1
                else:
                    self.app.fault = 0
                #if (self.app.n_SAT > 1):
                if keyboard.is_pressed('s'):
                    self.app.s_SAT = 1
                else:
                    self.app.s_SAT = 0
                self.app.time_now = time.strftime("%H:%M", time.localtime())

                """
                if (self.app.n_SAT > 1):
                    self.app.s_SAT = 0.8

                self.app.SOC = 2.1786 * self.app.V_BAT_HV - 147.06
                self.app.P_BRAKE = (counter * (self.app.limiterRpm / 6000))
                self.app.shiftRpm = (counter * (self.app.limiterRpm / 8000))
                self.app.Speed_km_h = counter
                self.apsp.time_now = time.strftime("%H:%M", time.localtime())
                self.app.LAP_TIME = str(format(time.perf_counter(), "0.2f"))
                

                H = self.app.V_BAT_HV
                if (H < 67.5):
                    H = 113.4
                self.app.V_BAT_HV = H - 0.0005 * t
                H = self.app.V_BAT_HV
                t = t + 1
                if (counter == 210):
                    counter = 0
                counter = counter + 1
                """
                time.sleep(0.01)



        except KeyboardInterrupt:
            # os.system("sudo /sbin/ip link set can0 down")
            print('\n\rKeyboard interrupt')


class DashApp(App):
    # ---Inverter---
    fault = NumericProperty(0)  # NumericProperty(0)
    # ---HV BATTERY
    V_BAT_HV = NumericProperty(114)  # NumericProperty(0)
    A_BAT_HV = NumericProperty(0)
    T_INV = NumericProperty(80)  # NumericProperty(0)
    # ---MOTOR
    VEL_RPM = NumericProperty(0)
    TRAC_DRIVE_S = NumericProperty(0)
    T_MOT = NumericProperty(97)  # NumericProperty(0)
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
    LAP_TIME = StringProperty(" ")  # NumericProperty(0)
    LAP_BEST = StringProperty("2:00:150")  # NumericProperty(0)
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
    V_BAT_LV = NumericProperty(12.5)  # NumericProperty(0)
    ODO = NumericProperty(10.1)

    # --- SENSORS---

    # ---BRAKE
    BRAKE = NumericProperty(0)
    # ---Acqua
    T_WATER = NumericProperty(92)  # NumericProperty(0)
    # ---Dinamica
    FRONT = StringProperty("20")  # NumericProperty(0)
    MONO = StringProperty("11")  # NumericProperty(0)
    # ---TIME %H:%M
    time_now = StringProperty(" ")
    ### useful vars
    s_SAT = NumericProperty(0)
    SOC = NumericProperty(0)
    t = NumericProperty(0)
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
        Clock.schedule_interval(sm.update, 0.005)

        return sm


if __name__ == '__main__':
    DashApp().run()
