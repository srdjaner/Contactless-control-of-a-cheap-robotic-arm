import sys
from PyQt4 import QtGui, QtCore
import Leap, sys, time
import numpy as np
from pyduino import *
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import math
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

l1=14.8
l2=16
#lengths of parts


class Window(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
    #DUGMICI
        self.quit_button = QtGui.QPushButton("Exit", self)
        self.quit_button.clicked.connect(self.close_application)
        #self.quit_button.resize(100, 50)
        #self.quit_button.move(0, 100)

        self.connect_button = QtGui.QPushButton("Start Leap", self)
        self.connect_button.clicked.connect(self.to_arduino)
        #self.connect_button.resize(100, 50)
        #self.connect_button.move(0, 150)
        self.connect_button.setStatusTip('Establish connection with arduino and begin')

        self.leap_button = QtGui.QPushButton("Stop Leap", self)
        self.leap_button.clicked.connect(self.break_leap)
        #self.leap_button.resize(100, 50)
        #self.leap_button.move(0, 200)
        self.leap_button.setStatusTip('Break connection with arduino')

    ###    
        
    #LABELS
        self.line_edit1=QtGui.QLineEdit('100',self)
        self.line_edit1.move(200,200)
        self.line_edit2=QtGui.QLineEdit('120',self)
        self.line_edit2.move(200,250)
        self.line_edit3=QtGui.QLineEdit('30',self)
        self.line_edit3.move(200,300)
        self.line_edit4=QtGui.QLineEdit('90',self)
        self.line_edit4.move(200,350)
        self.line_edit5=QtGui.QLineEdit('100',self)
        self.line_edit5.move(200,400)

        self.horizontal_layout = QtGui.QHBoxLayout()
        self.vertical1 = QtGui.QVBoxLayout()
        self.vertical2 = QtGui.QVBoxLayout()
        self.vertical3 = QtGui.QVBoxLayout()
        
        
        self.vertical1.addWidget(self.connect_button)
        self.vertical1.addWidget(self.leap_button)
        self.vertical1.addWidget(self.quit_button)

        self.vertical2.addWidget(self.line_edit1)
        self.vertical2.addWidget(self.line_edit2)
        self.vertical2.addWidget(self.line_edit3)
        self.vertical2.addWidget(self.line_edit4)
        self.vertical2.addWidget(self.line_edit5)

        self.vertical3.addWidget(self.toolbar)
        self.vertical3.addWidget(self.canvas)
        
        self.horizontal_layout.addLayout(self.vertical1)
        self.horizontal_layout.addLayout(self.vertical2)
        self.horizontal_layout.addLayout(self.vertical3)
        self.setLayout(self.horizontal_layout)
        
        self.setGeometry(50, 50, 600, 500)
        self.setWindowTitle("Leap Motion App")
        self.setWindowIcon(QtGui.QIcon('robot3.png'))
      
        self.check_listener = False
        self.plot()

    def plot(self):
        self.x1 = l1*math.cos(int(self.line_edit2.text())/57.2957795)
        self.x2 = self.x1 + l2*math.cos(int(self.line_edit3.text())/57.2957795)
        self.y1 = l1*math.sin(int(self.line_edit2.text())/57.2957795)
        self.y2 = self.y1 - l2*math.sin(int(self.line_edit3.text())/57.2957795)
        
        x=[0, self.x1, self.x2]
        y=[0, self.y1, self.y2]
        self.prev_x2 = [self.x2, self.x2, self.x2]
        self.prev_y2 = [self.y2, self.y2, self.y2]
        # create an axis
        #ax = self.figure.add_subplot(111)

        # discards the old graph
        plt.hold(False)
        
        plt.plot(x, y, '*-')
        # plot data
        #plt.plot(self.x2, self.y2, 'r')
        #plt.xlabel('length')
        #plt.ylabel('hight')

        axis = plt.gca()
        axis.set_xlim([-15,32])
        axis.set_ylim([-10, 20])

        # refresh canvas
        self.canvas.draw()

        self

    def draw_object(self, state):
        if state == QtCore.Qt.Checked:
            obj = self.figure.add_subplot(111)
            #obj.hold(False)
            obj.plot(self.x2+1, self.y2+1, 'r')
            self.canvas.draw()
        else:
            self.setGeometry(50, 50, 500, 300)

    def to_arduino(self):
        self.listener = LeapMotionListener()
        self.listener.signal_out1.connect(self.set_data1)
        self.listener.signal_out2.connect(self.set_data2)
        self.listener.signal_out3.connect(self.set_data3)
        self.listener.signal_out4.connect(self.set_data4)
        self.listener.signal_out5.connect(self.set_data5)
        self.check_listener = True
        self.plot()
        #self.controller = Leap.Controller()
        #self.controller.add_listener(self.listener)

    def set_data1(self, angle):
        value=str(angle)
        self.line_edit1.setText(value)

    def set_data2(self, angle):
        value=str(angle)
        self.line_edit2.setText(value)
        self.plot()

    def set_data3(self, angle):
        value=str(angle)
        self.line_edit3.setText(value)

    def set_data4(self, angle):
        value=str(angle)
        self.line_edit4.setText(value)

    def set_data5(self, angle):
        value=str(angle)
        self.line_edit5.setText(value)

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract!', "Are you sure?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print "Bye bye"
            if self.check_listener:
                self.listener.controller.remove_listener(self.listener)
            else:
                pass
            sys.exit()
        else:
            pass

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    def break_leap(self):
        self.listener.controller.remove_listener(self.listener)
        self.listener.signal_out1.connect(self.set_data1)
        self.listener.signal_out2.connect(self.set_data2)
        self.listener.signal_out3.connect(self.set_data3)
        self.listener.signal_out4.connect(self.set_data4)
        self.listener.signal_out5.connect(self.set_data5)
        self.plot()
        self.check_listener = False


class LeapMotionListener(Leap.Listener, QtCore.QObject):
    #finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    oldtime = time.time()
    newtime = time.time()
    signal_out1=QtCore.pyqtSignal(long)
    signal_out2=QtCore.pyqtSignal(long)
    signal_out3=QtCore.pyqtSignal(long)
    signal_out4=QtCore.pyqtSignal(long)
    signal_out5=QtCore.pyqtSignal(long)

    def __init__(self):
        super(LeapMotionListener, self).__init__()
        QtCore.QObject.__init__(self)
        self.controller = Leap.Controller()
        self.controller.add_listener(self)
       
    def on_init(self, controller):

        #connect arduino
        self.a = Arduino()
        #sleep to have time for establishing serial connection
        time.sleep(3)

        #define pins for servos
        self.SER1 = 11
        self.SER2 = 10
        self.SER3 = 9
        self.SER4 = 6
        self.SER5 = 5

        #previous state of servo 1
        self.prev_ser1 = 100
        self.new_ser1 = 100

        self.previous_angle = [100, 150, 60, 90, 100]

        #time to make connection
        time.sleep(1)
        print "Initiated"

    def on_connect(self, controller):
        print "Motion Sensor Connected!"

        #enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        time.sleep(1)
        # Reposition arm when program stopped

    #OVO MORA NEZNIJE
        self.a.servo_write(self.SER1, 100)
        self.a.servo_write(self.SER2, 150)
        self.a.servo_write(self.SER3, 60)
        self.a.servo_write(self.SER4, 90)
        self.a.servo_write(self.SER5, 100)

        self.signal_out1.emit(100)
        self.signal_out2.emit(150-30)
        self.signal_out3.emit(60-30)
        self.signal_out4.emit(90)
        self.signal_out5.emit(100)

        self.a.close()
        
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        interaction_box = frame.interaction_box
        
        self.newtime = time.time()
        #sampling 80ms and 2 hands problem
        if self.newtime - self.oldtime > 0.08 and len(controller.frame().hands) == 1:
        
            for hand in frame.hands:
                   
                normalized_point = interaction_box.normalize_point(hand.palm_position,True)
                #position in range 0 to 1
                self.XPOS = normalized_point.x
                self.YPOS = normalized_point.y
                self.ZPOS = normalized_point.z

                resolution = 0.01
                #new_x = int(round(self.XPOS/resolution))*resolution
                               
                x_vel = int(round(hand.palm_velocity.x/35)/resolution)*resolution
                #print "Velocity: " + str(x_vel)

                if abs(x_vel) > 1 :
                    
                    if self.prev_ser1 - x_vel < 0 or self.prev_ser1 - x_vel > 180:
                        self.new_ser1 = self.prev_ser1
                    else:
                        self.new_ser1 = self.prev_ser1 - x_vel
                        
                    self.prev_ser1 = self.new_ser1
                else:
                    pass
                
                Y=-6+normalized_point.y*20
                Z=10+abs(normalized_point.z-1)*20
                
                h=math.sqrt(Y*Y+Z*Z)
                a=math.atan(Y/Z)
                b=math.acos((l1*l1+h*h-l2*l2)/(2*l1*h))
                theta1=57.2957795*(a+b)
                c=math.acos((l2*l2+l1*l1-h*h)/(2*l1*l2))
                theta2=180-57.2957795*c
                s2=theta1+30
                s3=theta2-theta1+30

                print "Y: " + str(Y) + " , Z: " + str(Z)
                print "New angles are: " + str(s2) + " , " + str(s3)

                                               
                #HERE ARE CHANGES
                self.angle1 = int(abs(self.new_ser1))
                self.angle2 = int(s2) 
                self.angle3 = int(s3)
                self.angle4 = int(90 - hand.palm_normal.roll * Leap.RAD_TO_DEG)
                self.angle5 = 120 if hand.pinch_strength > 0.5 else 60
                #maybe can do better

                self.signal_out1.emit(self.angle1)
                self.signal_out2.emit(self.angle2-30)
                self.signal_out3.emit(self.angle3-30)
                self.signal_out4.emit(self.angle4)
                self.signal_out5.emit(self.angle5)

                print "Servo angles: " + str(int(self.angle1)) + ", " + str(int(self.angle2)) + ", " + str(int(self.angle3)) + ", " + str(int(self.angle5))
                
                self.a.servo_write(self.SER1, int(self.angle1))
                self.a.servo_write(self.SER2, int(self.angle2))
                self.a.servo_write(self.SER3, int(self.angle3))
                self.a.servo_write(self.SER4, int(self.angle4))                     
                self.a.servo_write(self.SER5, int(self.angle5))
                
                previous_angle = [self.angle1, self.angle2, self.angle3, 90, self.angle5]
                #reset oldtime
                self.oldtime = self.newtime
                
        else:
            pass
            #keep advancing until time difference 100ms
            


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    #GUI.home()
    GUI.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
