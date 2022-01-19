from tkinter import *
from tkinter import ttk
import serial
from serial.tools import list_ports
import sys
sys.path.append('.')
from classes.pump_class import Pump

class Pump_tab:
    def __init__(self,tabControl,pump):
        self.pump = pump
        self.tab = ttk.Frame(tabControl)
        tabControl.add(self.tab, text=pump.name)

        self.lock_button = self._lock_button()
        self.lock_button.grid(row=0,column=0,sticky=W,columnspan=2)

        self.unlock_button = self._unlock_button()
        self.unlock_button.grid(row=0,column=2,sticky=W,columnspan=2)

        self.stop_button = self._stop()
        self.stop_button.grid(row=0,column=4,sticky=W)

        self.flow_pane = self._flow_pane()
        self.flow_pane[0].grid(row=2,column=0,sticky=W)
        self.flow_pane[1].grid(row=2, column=1,sticky=W)
        self.flow_pane[2].grid(row=2,column=2,sticky=W)

        self.dispenseV_pane = self._dispenseV_pane()
        self.dispenseV_pane[0].grid(row=3,column=0,sticky=W)
        self.dispenseV_pane[1].grid(row=3,column=1,sticky=W)
        self.dispenseV_pane[2].grid(row=3,column=2, sticky=W)
        self.dispenseV_pane[3].grid(row=3, column=3,sticky=W)
        self.dispenseV_pane[4].grid(row=3,column=4, sticky=W)

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