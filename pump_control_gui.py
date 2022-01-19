from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_class import Pump
from functools import partial


fenetre = Tk()
fenetre.title("Gilson pumps control")
fenetre.geometry('500x300')

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
    tabs.append(ttk.Frame(tabControl))
    tabControl.add(tabs[-1], text=pumps[-1].name)

    #Lock button
    Button(tabs[-1],\
           text = 'Lock pump',\
           width = 20,\
           command = pumps[-1].lock)\
           .grid(row=0,column=0,sticky=W,columnspan=2)
    #Unlock button
    Button(tabs[-1],\
           text = 'Unlock pump',\
           width = 20,\
           command = pumps[-1].unlock)\
           .grid(row=0,column=2,sticky=W,columnspan=2)
    #Start flow
    flowrates.append(DoubleVar(value=0.000))
    ttk.Spinbox(tabs[-1],\
                from_ = 0,\
                to = 5,\
                increment = 0.001,\
                textvariable = flowrates[tabControl.index(tabControl.select())-1],\
                width=10)\
                .grid(row=2,column=0)

    Label(tabs[-1],text = 'mL/min', width=10).grid(row=2, column=1,sticky=W)

    def _start_flow():
        flowrate = flowrates[tabControl.index(tabControl.select())-1].get()
        pumps[tabControl.index(tabControl.select())-1].start_flow(flowrate)

    Button(tabs[-1],\
           text = 'Start flow',\
           command = _start_flow).grid(row=2,column=2)

    #Stop pumping
    Button(tabs[-1],\
           text = 'Stop pump',\
           width = 20,\
           bg = 'red',\
           command = pumps[tabControl.index(tabControl.select())-1].stop)\
           .grid(row=0,column=4,sticky=W,)

    #Dispense by Volume
    flowrates_dispenseV.append(DoubleVar(value=0.000))
    ttk.Spinbox(tabs[-1],\
                from_ = 0,\
                to = 5,\
                increment = 0.001,\
                textvariable = flowrates_dispenseV[tabControl.index(tabControl.select())-1],\
                width=10)\
                .grid(row=3,column=0)
    Label(tabs[-1],text = 'mL/min', width=10).grid(row=3,column=1)

    volumes.append(DoubleVar(value=0.000))
    ttk.Spinbox(tabs[-1],\
                from_ = 0,\
                to = 100,\
                increment = 0.001,\
                textvariable=volumes[tabControl.index(tabControl.select())-1],\
                width=10)\
                .grid(row=3,column=2)
    Label(tabs[-1],text = 'mL', width=10).grid(row=3, column=3,sticky=W)

    def _start_dispenseV():
        flowrate = flowrates_dispenseT[tabControl.index(tabControl.select())-1].get()
        time = times[tabControl.index(tabControl.select())-1].get()
        pumps[tabControl.index(tabControl.select())-1].dispense_volume(volume,flowrate)

    Button(tabs[-1],\
           text = 'Dispense volume',\
           command = _start_dispenseV)\
           .grid(row=3,column=4)


    #Dispense by Time
    flowrates_dispenseT.append(DoubleVar(value=0.000))
    ttk.Spinbox(tabs[-1],\
                from_ = 0,\
                to = 5,\
                increment = 0.001,\
                textvariable = flowrates_dispenseT[tabControl.index(tabControl.select())-1],\
                width=10)\
                .grid(row=4,column=0)
    Label(tabs[-1],text = 'mL/min', width=10).grid(row=4,column=1)

    times.append(DoubleVar(value=0.000))
    ttk.Spinbox(tabs[-1],\
                from_ = 0,\
                to = 100,\
                increment = 0.001,\
                textvariable=times[tabControl.index(tabControl.select())-1],\
                width=10)\
                .grid(row=4,column=2)
    Label(tabs[-1],text = 'min', width=10).grid(row=4, column=3,sticky=W)

    def _start_dispenseT():
        flowrate = flowrates_dispenseT[tabControl.index(tabControl.select())-1].get()
        time = times[tabControl.index(tabControl.select())-1].get()
        pumps[tabControl.index(tabControl.select())-1].dispense_duration(time,flowrate)

    Button(tabs[-1],\
           text = 'Dispense duration',\
           command = _start_dispenseT)\
           .grid(row=4,column=4)

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