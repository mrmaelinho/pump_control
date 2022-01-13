import serial
import time
import datetime

class Pump:
    """
    This class represents a Gilson Verity 3011 isocratic pump connected to a PC
    on a serial COM port via RS232-to-USB converter.
    Pump's main attribute self.ser is a serial.Serial instance.
    """

    def __init__(self,port_name):
        self.ser = serial.Serial(port=port_name,\
                                    baudrate=115200,\
                                    # parity=PARITY_NONE,\
                                    # bytesize=EIGHTBITS,\
                                    dsrdtr=True,\
                                    rtscts=True,\
                                    # stopbits=STOPBITS_ONE,\
                                    timeout=1)
        self.ser.close()

    def lock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Lock)]?\r\n'.encode())
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('{} Pump locked'.format(ts))

    def unlock(self):
        self.ser.open()
        self.ser.write('?[1007,0,1,CMD,SYN,0(Unlock)]?\r\n'.encode())
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('{} Pump unlocked'.format(ts))

    def flow(self,flowrate):
        self.ser.open()
        message = '?[1002,0,1,CMD,SYN,0(Set Pump Flow Rate,%.3f)]?\r\n'%flowrate
        self.ser.write(message.encode())
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('{} Pumping at {} mL/min'.format(ts, flowrate))

    def stop(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop Pump,false)]?\r\n'.encode())
        self.ser.close()
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print('{} Pump stopped'.format(ts))

    def start_pressure_samples(self,datapoint_interval):
        message = '?[1003,0,1,CMD,SYN,0(Start pressure samples,{},1)]?\r\n'.format(datapoint_interval)
        self.ser.open()
        self.ser.write(message.encode())
        self.ser.close()
        print('{} Started pressure sampling every {} ms'.format(ts,datapoint_interval))

    def stop_pressure_samples(self):
        self.ser.open()
        self.ser.write('?[1003,0,1,CMD,SYN,0(Stop)]?\r\n'.encode())
        self.ser.close()
        print('{} Stopped pressure sampling'.format(ts))

    def read_messages(self,duration):
        self.ser.open()
        t0 = time.time()
        t = t0
        while (t-t0) < duration:
            if self.ser.inWaiting() > 0:
                self.ser.readline()
        self.ser.close()

# if __name__ == "__main__":
#     pump1 = serial.Serial(port='COM9',\
#                           baudrate=115200,\
#                         # parity=PARITY_NONE,\
#                         # bytesize=EIGHTBITS,\
#                           dsrdtr=True,\
#                           rtscts=True,\
#                         # stopbits=STOPBITS_ONE,\
#                           timeout=1)
#     pump1.close()