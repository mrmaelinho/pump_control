import serial
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Pump:
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
                                    timeout=0.5)
        self.ser.close()
        self.name = pump_name
        self.pressure = list()
        self.t = list()

    def open(self):
        self.ser.open()
        buff = self.ser.readall()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is open.'.format(ts,self.name))

    def close(self):
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} communication is closed.'.format(ts,self.name))

    def lock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Lock)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} locked.'.format(ts,self.name))

    def unlock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Unlock)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} unlocked.'.format(ts,self.name))

    def start_flow(self,flowrate):
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
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Dispense by Volume,%.3f,%.3f)]?\r\n'%(flowrate,volume)
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing {} mL at {} mL/min.'.format(ts, self.name, volume, flowrate))

    def dispense_duration(self, duration, flowrate):
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Dispense by Time,%.3f,%.2f)]?\r\n'%(flowrate,duration)
        self.ser.write(message.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} dispensing at {} mL/min during {} min.'.format(ts, self.name, flowrate, duration))

    def stop(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop Pump,false)]?\r\n'.encode())
        self.ser.close()
        self.ser.open()
        buff = self.ser.readall()
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(buff.decode())
        print('{} {} stopped.'.format(ts,self.name))

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
        buff = self.ser.readall()
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
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        # print(buff.decode())
        _pressure = float(buff.decode()[-10:-5])
        # print('{} {} has pressure {} bar.'.format(ts, self.name, _pressure))
        return _pressure

    def read_messages(self,duration):
        self.ser.open()
        t0 = time.time()
        t = t0
        while (t-t0) < duration:
            if self.ser.inWaiting() > 0:
                self.ser.readline()
        self.ser.close()

    def plot_pressure(self,frame,t0, ax, pressure_line):
        self.pressure.append(pump1.get_pressure())
        self.t.append(time.time()-t0)
        ax.set_xlim(0,self.t[-1])
        pressure_line.set_data(self.t,self.pressure)
        return ax,

def anim_pressure(pump):
    t0 = time.time()
    pressure = list()
    t = list()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('{} pressure'.format(pump.name))
    ax.set_ylim(0,40)
    ax.grid()
    pressure_line, = ax.plot([],[],label='pump pressure')
    anim = animation.FuncAnimation(fig, pump.plot_pressure, fargs=[t0, ax, pressure_line], frames=None, blit=False, interval=25, repeat=True)
    fig.show()
    return anim

if __name__ == "__main__":
    pump1 = Pump('COM9','Pump 1')
