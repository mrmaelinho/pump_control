#author : Maël Arveiler
from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_classes import Pump_Gilson, Pump_LSPOne

class Pump_tab_Gilson:
    """
    Instance creating a tab containing the Tk widgets to control
    the pump (of class Pump) to which the tab is associated.
    The commands associated to the widgets are Pump attributes.
    """
    def __init__(self,tabControl,pump):
        self.pump = pump
        #Creates a new tab associated to the pump
        self.tab = ttk.Frame(tabControl)
        tabControl.add(self.tab, text=pump.name)

        #Lock button
        self.lock_button = self._lock_button()
        self.lock_button.grid(row=0,column=0,sticky=W,columnspan=2)

        #Unlock button
        self.unlock_button = self._unlock_button()
        self.unlock_button.grid(row=0,column=2,sticky=W,columnspan=2)

        #Stop button
        self.stop_button = self._stop()
        self.stop_button.grid(row=0,column=4,sticky=W)

        #Section with flowrate selection and start flow button
        self.flow_pane = self._flow_pane()
        self.flow_pane[0].grid(row=2,column=0,sticky=W)
        self.flow_pane[1].grid(row=2,column=1,sticky=W)
        self.flow_pane[2].grid(row=2,column=2,sticky=W)

        #Section with flowrate and volume selection and dispense volume button
        self.dispenseV_pane = self._dispenseV_pane()
        self.dispenseV_pane[0].grid(row=3,column=0,sticky=W)
        self.dispenseV_pane[1].grid(row=3,column=1,sticky=W)
        self.dispenseV_pane[2].grid(row=3,column=2, sticky=W)
        self.dispenseV_pane[3].grid(row=3, column=3,sticky=W)
        self.dispenseV_pane[4].grid(row=3,column=4, sticky=W)

        #Section with flowrate and duration selection and dispense duration button
        self.dispenseT_pane = self._dispenseT_pane()
        self.dispenseT_pane[0].grid(row=4,column=0,sticky=W)
        self.dispenseT_pane[1].grid(row=4,column=1,sticky=W)
        self.dispenseT_pane[2].grid(row=4,column=2, sticky=W)
        self.dispenseT_pane[3].grid(row=4, column=3,sticky=W)
        self.dispenseT_pane[4].grid(row=4,column=4, sticky=W)


    def _lock_button(self):
        return Button(self.tab,\
                      text = 'Lock pump',\
                      width = 20,\
                      command = self.pump.lock)

    def _unlock_button(self):
        return Button(self.tab,\
                      text = 'Unlock pump',\
                      width = 20,\
                      command = self.pump.unlock)
    def _stop(self):
        return Button(self.tab,\
                      text = 'Stop pump',\
                      width = 20,\
                      bg = 'red',\
                      command = self.pump.stop)

    def _flow_pane(self):
        self.flowrate = DoubleVar(value=0.000)
        self.flow_spinbox = ttk.Spinbox(self.tab,\
                              from_ = 0,\
                              to = 5,\
                              increment = 0.001,\
                              textvariable = self.flowrate,\
                              width=10)
        self.flowrate_label = Label(self.tab,text = 'mL/min', width=10)
        def _start_flow():
            flowrate = self.flowrate.get()
            self.pump.start_flow(flowrate)
        self.flow_button = Button(self.tab,\
                                  text = 'Start flow',\
                                  command = _start_flow)
        return (self.flow_spinbox,\
                self.flowrate_label,\
                self.flow_button)

    def _dispenseV_pane(self):
        self.flowrateV = DoubleVar(value=0.000)
        self.flowrateV_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 5,\
                                             increment = 0.001,\
                                             textvariable = self.flowrateV,\
                                             width=10)
        self.flowrate_dispenseV_label = Label(self.tab,\
                                              text = 'mL/min',\
                                              width=10)
        self.volume = DoubleVar(value=0.000)
        self.dispenseV_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 100,\
                                             increment = 0.001,\
                                             textvariable=self.volume,\
                                             width=10)
        self.dispenseV_label = Label(self.tab,text = 'mL', width=10)
        def _start_dispenseV():
            flowrate = self.flowrateV.get()
            volume = self.volume.get()
            self.pump.dispense_volume(volume,flowrate)
        self.dispenseV_button = Button(self.tab,\
                                       text = 'Dispense volume',\
                                       command = _start_dispenseV)
        return (self.flowrateV_spinbox,\
                self.flowrate_dispenseV_label,\
                self.dispenseV_spinbox,\
                self.dispenseV_label,\
                self.dispenseV_button)

    def _dispenseT_pane(self):
        self.flowrateT = DoubleVar(value=0.000)
        self.flowrateT_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 5,\
                                             increment = 0.001,\
                                             textvariable = self.flowrateT,\
                                             width=10)
        self.flowrate_dispenseT_label = Label(self.tab,\
                                              text = 'mL/min',\
                                              width=10)
        self.duration = DoubleVar(value=0.000)
        self.dispenseT_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 100,\
                                             increment = 0.001,\
                                             textvariable=self.duration,\
                                             width=10)
        self.dispenseT_label = Label(self.tab,text = 'min', width=10)
        def _start_dispenseT():
            flowrate = self.flowrateT.get()
            duration = self.duration.get()
            self.pump.dispense_duration(duration,flowrate)
        self.dispenseT_button = Button(self.tab,\
                                       text = 'Dispense duration',\
                                       command = _start_dispenseT)
        return (self.flowrateT_spinbox,\
                self.flowrate_dispenseT_label,\
                self.dispenseT_spinbox,\
                self.dispenseT_label,\
                self.dispenseT_button)

class Pump_tab_LSPOne:
    """
    Instance creating a tab containing the Tk widgets to control
    the pump (of class Pump) to which the tab is associated.
    The commands associated to the widgets are Pump attributes.
    """
    def __init__(self,tabControl,pump):
        self.pump = pump
        #Creates a new tab associated to the pump
        self.tab = ttk.Frame(tabControl)
        tabControl.add(self.tab, text=pump.name)

        #Stop button
        self.stop_button = self._stop()#Create button
        self.stop_button.grid(row=0,\
                              column=0,\
                              columnspan=2,\
                              sticky=W)#pack button in grid

        #Syringe size selection
        self.syringe_select = self._syringe_selection()
        for i in range(2):#pack all the widgets in the grid
            self.syringe_select[i].grid(row=2,column=i,sticky=W)

        #Solvent and waste ports
        self.standard_ports = self._ports_selection()
        for i in range(4):#pack all the widgets in the grid
            self.standard_ports[i].grid(row=3,column=i,sticky=W)

        #Section with flowrate and volume selection and dispense volume button
        self.dispenseV_pane = self._dispenseV_pane()#create all the widgets
        for i in range(9):#pack all the widgets in the grid
            self.dispenseV_pane[i].grid(row=4,column=i,sticky=W)

    def _stop(self):
        return Button(self.tab,\
                      text = 'Stop pump',\
                      width = 20,\
                      bg = 'red',\
                      command = self.pump.stop)

    def _syringe_selection(self):
        syringe_V_choices = [50,1000]
        syringe_V_labels = ['50 µL', '1000 µL']
        self.syringe_V = IntVar()
        self.syringe_V.set(syringe_V_choices[1])
        syringe_button = list()
        for i in range(2):
            syringe_button.append(ttk.Radiobutton(self.tab,\
                                  variable=self.syringe_V,\
                                  text=syringe_V_labels[i],\
                                  value=syringe_V_choices[i]))
        return syringe_button

    def _ports_selection(self):
        self.solvent_port_label = ttk.Label(self.tab,\
                                        text='Fresh solvent port',\
                                        width=10)
        self.solvent_port = IntVar(value=1)
        self.solvent_port_spinbox = ttk.Spinbox(self.tab,\
                                          from_ =1,\
                                          to = 8,\
                                          increment=1,\
                                          textvariable = self.solvent_port,\
                                          width=10)
        self.waste_port_label = ttk.Label(self.tab,\
                                        text='Waste port',\
                                        width=10)
        self.waste_port = IntVar(value=8)
        self.waste_port_spinbox = ttk.Spinbox(self.tab,\
                                          from_ =1,\
                                          to = 8,\
                                          increment=1,\
                                          textvariable = self.waste_port,\
                                          width=10)
        return (self.solvent_port_label,\
                self.solvent_port_spinbox,\
                self.waste_port_label,\
                self.waste_port_spinbox)

    def _dispenseV_pane(self):
        self.port_in_label = ttk.Label(self.tab,\
                                  text="In port",\
                                  width = 10)
        self.port_in = IntVar(value=1)
        self.port_in_spinbox = ttk.Spinbox(self.tab,\
                                          from_ =1,\
                                          to = 8,\
                                          increment=1,\
                                          textvariable = self.port_in,\
                                          width=10)

        self.port_out_label = ttk.Label(self.tab,\
                                  text="Out port",\
                                  width = 10)
        self.port_out = IntVar(value=2)
        self.port_out_spinbox = ttk.Spinbox(self.tab,\
                                          from_ =1,\
                                          to = 8,\
                                          increment=1,\
                                          textvariable = self.port_out,\
                                          width=10)
        self.flowrateV = DoubleVar(value=0.000)
        self.flowrateV_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 1,\
                                             to = 5000,\
                                             increment = 1,\
                                             textvariable = self.flowrateV,\
                                             width=10)
        self.flowrate_dispenseV_label = ttk.Label(self.tab,\
                                              text = 'µL/min',\
                                              width=10)
        self.volume = DoubleVar(value=0.000)
        self.dispenseV_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 10000,\
                                             increment = 1,\
                                             textvariable=self.volume,\
                                             width=10)
        self.dispenseV_label = ttk.Label(self.tab,\
                                     text = 'µL',\
                                     width=15)

        def _start_dispenseV():
            self.pump.dispense_volume(self.port_in.get(),\
                                      self.port_out.get(),\
                                      self.volume.get(),\
                                      self.flowrateV.get(),\
                                      self.syringe_V.get())

        self.dispenseV_button = ttk.Button(self.tab,\
                                       text = 'Dispense volume',\
                                       command = _start_dispenseV)
        return (self.port_in_label,\
                self.port_in_spinbox,\
                self.port_out_label,\
                self.port_out_spinbox,\
                self.flowrateV_spinbox,\
                self.flowrate_dispenseV_label,\
                self.dispenseV_spinbox,\
                self.dispenseV_label,\
                self.dispenseV_button)


    def _dispenseT_pane(self):
        self.flowrateT = DoubleVar(value=0.000)
        self.flowrateT_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 5,\
                                             increment = 0.001,\
                                             textvariable = self.flowrateT,\
                                             width=10)
        self.flowrate_dispenseT_label = Label(self.tab,\
                                              text = 'mL/min',\
                                              width=10)
        self.duration = DoubleVar(value=0.000)
        self.dispenseT_spinbox = ttk.Spinbox(self.tab,\
                                             from_ = 0,\
                                             to = 100,\
                                             increment = 0.001,\
                                             textvariable=self.duration,\
                                             width=10)
        self.dispenseT_label = Label(self.tab,text = 'min', width=10)
        def _start_dispenseT():
            flowrate = self.flowrateT.get()
            duration = self.duration.get()
            self.pump.dispense_duration(duration,flowrate)
        self.dispenseT_button = Button(self.tab,\
                                       text = 'Dispense duration',\
                                       command = _start_dispenseT)
        return (self.flowrateT_spinbox,\
                self.flowrate_dispenseT_label,\
                self.dispenseT_spinbox,\
                self.dispenseT_label,\
                self.dispenseT_button)
