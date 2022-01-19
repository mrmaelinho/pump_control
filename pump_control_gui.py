from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_class import Pump


fenetre = Tk()
fenetre.title("Gilson pumps control")
fenetre.geometry('300x300')

tabControl = ttk.Notebook(fenetre)
tabs = list()

## tabs[0] : Connect pump
tabs.append(ttk.Frame(tabControl))
tabControl.add(tabs[0], text='Connect pump')

ports = list_ports.comports()
ports.pop(0)
ports_list = Listbox(tabs[0],width=30)
for port in ports:
    ports_list.insert(ports.index(port),port.description)
ports_list.pack()

pumps = list()

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
    tabs.append(ttk.Frame(tabControl))
    tabControl.add(tabs[-1], text=pumps[-1].name)

    #Lock button
    lock_button = Button(tabs[-1],\
                        text = 'Lock pump',\
                        width = 20,\
                        command = pumps[-1].lock)
    lock_button.grid(row=0,column=0,sticky=W,columnspan=2)
    #Unlock button
    unlock_button = Button(tabs[-1],\
                        text = 'Unlock pump',\
                        width = 20,\
                        command = pumps[-1].unlock)
    unlock_button.grid(row=1,column=0,sticky=W,columnspan=2)
    #Start flow
    flowrate_value = StringVar(value=0.000)
    flowrate_spinbox = ttk.Spinbox(tabs[-1],\
                               from_ = 0,\
                               to = 5,\
                               increment = 0.001,\
                               textvariable = flowrate_value,\
                               width=10)
    flowrate_spinbox.grid(row=2,column=0)
    flowrate_label = Label(tabs[-1],text = 'mL/min', width=10)
    flowrate_label.grid(row=2, column=1,sticky=W)
    start_flow_button = Button(tabs[-1],\
                               text = 'Start flow',\
                               command = lambda : pumps[-1].start_flow(float(flowrate_value.get())))
    start_flow_button.grid(row=2,column=2)
    #Dispense by Volume
    flowrate_value_dispenseV = StringVar(value=0.000)
    flowrate_spinbox_dispenseV = ttk.Spinbox(tabs[-1],\
                               from_ = 0,\
                               to = 5,\
                               increment = 0.001,\
                               textvariable = flowrate_value_dispenseV,\
                               width=10)
    flowrate_spinbox_dispenseV.grid(row=3,column=0)
    flowrate_label_dispenseV = Label(tabs[-1],text = 'mL/min', width=10)
    flowrate_label_dispenseV.grid(row=3,column=1)

    volume_value = StringVar(value=0.000)
    volume_spinbox = ttk.Spinbox(tabs[-1],\
                               from_ = 0,\
                               to = 100,\
                               increment = 0.001,\
                               textvariable = volume_value,\
                               width=10)
    volume_spinbox.grid(row=3,column=2)
    volume_label = Label(tabs[-1],text = 'mL', width=10)
    volume_label.grid(row=3, column=3,sticky=W)

    start_dispenseV_button = Button(tabs[-1],\
                               text = 'Dispense volume',\
                               command = lambda : pumps[-1].dispense_volume(float(volume_value.get()),float(flowrate_value_dispenseV.get())))
    start_dispenseV_button.grid(row=3,column=4)
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