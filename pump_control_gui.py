from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_class import Pump
from classes.pump_tab_class import Pump_tab
from functools import partial

def test_is_pump(com):
    """
    Determines if the COM port selected for connection is a pump.
    """
    #Establish a serial connection with pump parameters.
    test_port = serial.Serial(port=com,\
                        baudrate=115200,\
                        # parity=PARITY_NONE,\
                        # bytesize=EIGHTBITS,\
                        dsrdtr=True,\
                        rtscts=True,\
                        # stopbits=STOPBITS_ONE,\
                        timeout=1)
    #Send command to retrieve Device ID, will answer only if device is a pump.
    test_port.write('?[1001,0,1,CMD,SYN,0(Get Device ID)]?\r\n'.encode())
    test_port.close()
    test_port.open()
    buff = test_port.readline()
    test_port.close()
    #Expected answer contains the name of the pump
    if buff.decode()[-35:-5] == 'VERITY 3011 CONTROLLER,1.1.0.0':
        return True
    else:
        return False

def test_already_connected(com):
    """
    Determines if the COM port selected for connection is already connected.
    """
    already_connected = False
    #Loop goes through list of pumps already connected\
    #and checks if one is connected on the selected COM port.
    for pump in pumps:
        if pump.ser.port == com:
            already_connected = True
            break
    return already_connected

def create_pump_tab():
    """
    Creates a new tab with controls for the newly connected pump.
    Each tab is a Pump_tab class instance.
    """
    tabs.append(Pump_tab(tabControl,pumps[-1]))


def connect_pump():
    """
    When "connect" button is pressed, checks if the selected port
    is not already connected, then checks if the device on selected port
    is a controllable pump.
    If both are true, establishes the connection with the pump. 
    """
    #Gets the port selected in the available COM ports list.
    to_connect = ports_list.curselection()
    print('Connecting',ports[to_connect[0]],'...')
    
    #Check if the COM port is already connected.
    already_connected = test_already_connected(ports[to_connect[0]].name)
    if already_connected:
        print(ports[to_connect[0]].name,'is already connected...')
    else :
        #Check if device on COM port is a controllable pump.
        port_is_pump = test_is_pump(ports[to_connect[0]].name)
        if port_is_pump:
            #Create a new Pump instance, together with a new Pump_tab instance.
            pump_number = str(len(pumps)+1)
            pumps.append(Pump(ports[to_connect[0]].name,'Pump '+str(len(pumps)+1)))
            print('Success :',ports[to_connect[0]].name,'connected as Pump',len(pumps))
            create_pump_tab()
        else:
            print('Device on port %s is not detected as a pump'%ports[to_connect[0]].name)

if __name__ == '__main__':        
    #Main GUI window.
    fenetre = Tk()
    fenetre.title("Gilson pumps control")
    fenetre.geometry('500x300')

    #Notebook filled with tabs (first a "connect pump tab" then a tab for each pump).
    tabControl = ttk.Notebook(fenetre)
    tabControl.pack(expand=1, fill="both")
    tabs = list()

    #First tab : connect pumps.
    tabs.append(ttk.Frame(tabControl))
    tabControl.add(tabs[0], text='Connect pump')
    
    #Lists available COM ports in first tab.
    ports = list_ports.comports()
    ports.pop(0)#Removes COM1 which is internal and cannot communicate.
    ports_list = Listbox(tabs[0],width=30)#Display list of avilable COM ports.
    for port in ports:
        ports_list.insert(ports.index(port),port.description)
    ports_list.pack()
    
    #Container for pumps (of class Pump) that are connected.
    pumps = list()
    
    #Button to connect the pump selected in the list of available COM ports.
    connect_button = Button(tabs[0],text='Connect', command = connect_pump).pack()  

    fenetre.mainloop()
