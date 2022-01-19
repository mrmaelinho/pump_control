from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_class import Pump
from classes.pump_tab_class import Pump_tab
from functools import partial


fenetre = Tk()
fenetre.title("Gilson pumps control")
fenetre.geometry('500x300')

tabControl = ttk.Notebook(fenetre)
tabs = list()

tabs.append(ttk.Frame(tabControl))
tabControl.add(tabs[0], text='Connect pump')

ports = list_ports.comports()
ports.pop(0)
ports_list = Listbox(tabs[0],width=30)
for port in ports:
    ports_list.insert(ports.index(port),port.description)
ports_list.pack()

pumps = list()
flowrates = list()
flowrates_dispenseV = list()
flowrates_dispenseT = list()
volumes = list()
times = list()

def test_is_pump(com):
    test_port = serial.Serial(port=com,\
                        baudrate=115200,\
                        # parity=PARITY_NONE,\
                        # bytesize=EIGHTBITS,\
                        dsrdtr=True,\
                        rtscts=True,\
                        # stopbits=STOPBITS_ONE,\
                        timeout=1)
    test_port.write('?[1001,0,1,CMD,SYN,0(Get Device ID)]?\r\n'.encode())
    test_port.close()
    test_port.open()
    buff = test_port.readline()
    test_port.close()
    if buff.decode()[-35:-5] == 'VERITY 3011 CONTROLLER,1.1.0.0':
        return True
    else:
        return False

def test_already_connected(com):
    already_connected = False
    for pump in pumps:
        if pump.ser.port == com:
            already_connected = True
            break
    return already_connected

def create_pump_tab():
    tabs.append(Pump_tab(tabControl,pumps[-1]))


def connect_pump():
    to_connect = ports_list.curselection()
    print('Connecting',ports[to_connect[0]],'...')
    already_connected = test_already_connected(ports[to_connect[0]].name)
    if already_connected:
        print(ports[to_connect[0]].name,'is already connected...')
    else :
        port_is_pump = test_is_pump(ports[to_connect[0]].name)
        if port_is_pump:
            pump_number = str(len(pumps)+1)
            pumps.append(Pump(ports[to_connect[0]].name,'Pump '+str(len(pumps)+1)))
            print('Success :',ports[to_connect[0]].name,'connected as Pump',len(pumps))
            create_pump_tab()
        else:
            print('Device on port %s is not detected as a pump'%ports[to_connect[0]].name)

connect_button = Button(tabs[0],text='Connect', command = connect_pump).pack()


tabControl.pack(expand=1, fill="both")

fenetre.mainloop()