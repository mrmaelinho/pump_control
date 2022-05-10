#author : Maël Arveiler
import serial
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

##Gilson
class Pump_Gilson:
    """
    This class represents a Gilson Verity 3011 isocratic pump connected to a PC
    on a serial COM port via RS232-to-USB converter.
    Pump's main attribute self.ser is a serial.Serial instance.
    """

    def __init__(self,port_name, pump_name):
        self.ser = serial.Serial(port=port_name,\
                                    baudrate=115200,\
                                    # parity=PARITY_NONE,\
                                    # bytesize=EIGHTBITS,\
                                    dsrdtr=True,\
                                    rtscts=True,\
                                    # stopbits=STOPBITS_ONE,\
                                    timeout=1)
        self.ser.close()
        self.name = pump_name
        self.pressure = [0]
        self.flowrate = [0]
        self.t = [0]

    def open(self):
        self.ser.open()
        buff = self.ser.readline()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is open.'.format(ts,self.name))

    def close(self):
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is closed.'.format(ts,self.name))

    def lock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Lock)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} locked.'.format(ts,self.name))

    def unlock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Unlock)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} unlocked.'.format(ts,self.name))

    def start_flow(self,flowrate):
        self.lock()
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Set Pump Flow Rate,%.3f)]?\r\n'%flowrate
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} pumping at {} mL/min.'.format(ts, self.name, flowrate))

    def dispense_volume(self, volume, flowrate):
        self.lock()
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Dispense by Volume,%.3f,%.3f)]?\r\n'%(flowrate,volume)
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing {} mL at {} mL/min.'.format(ts, self.name, volume, flowrate))

    def dispense_duration(self, duration, flowrate):
        self.lock()
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Dispense by Time,%.3f,%.2f)]?\r\n'%(flowrate,duration)
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing at {} mL/min during {} min.'.format(ts, self.name, flowrate, duration))

    def stop(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop Pump,false)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} stopped.'.format(ts,self.name))
        self.unlock()

    def start_pressure_samples(self,datapoint_interval):
        message = '?[1003,0,1,CMD,SYN,0(Start pressure samples,{},1)]?\r\n'.format(datapoint_interval)
        self.ser.open()
        self.ser.write(message.encode())
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        print(buff.decode())
        print('{} {} started pressure sampling every {} ms.'.format(ts,self.name,datapoint_interval))

    def stop_pressure_samples(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} stopped pressure sampling.'.format(ts, self.name))

    def get_pressure(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Get Pressure)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        #ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        # print(buff.decode())
        try:
            _pressure = float(buff.decode()[-10:-5])
        except ValueError:
            _pressure = self.pressure[-1]

        # print('{} {} has pressure {} bar.'.format(ts, self.name, _pressure))
        return _pressure

    def get_flowrate(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Get Pump Flow Rate)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        # ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        # print(buff.decode())
        try:
            _flowrate = float(buff.decode()[-10:-5])
        except ValueError:
            _flowrate = self.flowrate[-1]
        # print('{} {} has pressure {} bar.'.format(ts, self.name, _flowrate)
        return _flowrate

    def read_messages(self,duration):
        self.ser.open()
        t0 = time.time()
        t = t0
        while (t-t0) < duration:
            if self.ser.inWaiting() > 0:
                self.ser.readline()
        self.ser.close()

    def plot_pressure_flowrate(self,frame,t0, ax1, ax2, pressure_line, flowrate_line):
        self.pressure.append(self.get_pressure())
        time.sleep(3)
        self.flowrate.append(self.get_flowrate())
        self.t.append(time.time()-t0)
        ax2.set_xlim(0,self.t[-1])
        ax1.sharex(ax2)
        pressure_line.set_data(self.t,self.pressure)
        flowrate_line.set_data(self.t,self.flowrate)
        return ax1,ax2

def anim_pressure(pump):
    t0 = time.time()
    pressure = list()
    t = list()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.set_title('{} pressure'.format(pump.name))
    ax1.set_ylim(0,40)
    ax1.grid()
    ax1.set_xticklabels([])
    pressure_line, = ax1.plot([],[],label='pump pressure')
    ax2 = fig.add_subplot(212)
    ax2.set_title('{} flowrate'.format(pump.name))
    ax2.set_ylim(0,5)
    ax2.grid()
    flowrate_line, = ax2.plot([],[],label='pump flowrate')
    anim = animation.FuncAnimation(fig, pump.plot_pressure_flowrate, fargs=[t0, ax1, ax2, pressure_line, flowrate_line], frames=None, blit=False, interval=5000, repeat=True)
    fig.show()
    return anim

##LSPOne

class Pump_LSPOne:
    """
    This class represents a AMF LSPOne syringe pump connected to a PC
    on a serial COM port via RS232-to-USB converter.
    Pump's main attribute self.ser is a serial.Serial instance.
    """

    def __init__(self,port_name, pump_name):
        self.ser = serial.Serial(port=port_name,\
                                    baudrate=9600,\
                                    # parity=PARITY_NONE,\
                                    # bytesize=EIGHTBITS,\
                                    dsrdtr=True,\
                                    rtscts=True,\
                                    # stopbits=STOPBITS_ONE,\
                                    timeout=1)
        self.ser.close()
        self.name = pump_name

    def open(self):
        self.ser.open()
        buff = self.ser.readline()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is open.'.format(ts,self.name))

    def close(self):
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is closed.'.format(ts,self.name))

    def dispense_volume(self, port_in, port_out, volume, flowrate, syringe_V):
        self.ser.open()
        repetitions, rest = volume//syringe_V, volume%syringe_V
        speed = int((flowrate/60)/(syringe_V/3000))
        message='/1' #message initialisation
        if repetitions>0:
            message += 'gO%dN0V1600A3000O%dV%dA0G%d'%(port_in,\
                                                       port_out,\
                                                       speed,\
                                                       repetitions)
        if rest!=0:
            #Calculate number of syringe microsteps to pick desired volume
            message += 'O%dN0V1600A%dO%dV%dA0'%(port_in,\
                                                int(rest*3000/syringe_V),\
                                                port_out,\
                                                speed)
        message += 'R\r\n' #EOL characters
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing {} µL at {} mL/min.'.format(ts, self.name, volume, flowrate))

    def dispense_duration(self, duration, flowrate):
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Dispense by Time,%.3f,%.2f)]?\r\n'%(flowrate,duration)
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing at {} mL/min during {} min.'.format(ts, self.name, flowrate, duration))

    def stop(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop Pump,false)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readline()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} stopped.'.format(ts,self.name))
        self.unlock()
