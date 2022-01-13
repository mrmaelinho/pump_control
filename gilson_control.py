import serial
import time
import datetime


def lock(ser):
    ser.open()
    ser.write('?[1007,0,1,CMD,SYN,0(Lock)]?\r\n'.encode())
    ser.close()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('{} Pump locked'.format(ts))

def unlock(ser):
    ser.open()
    ser.write('?[1007,0,1,CMD,SYN,0(Unlock)]?\r\n'.encode())
    ser.close()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('{} Pump unlocked'.format(ts))

def flow(ser,flowrate):
    ser.open()
    message = '?[1002,0,1,CMD,SYN,0(Set Pump Flow Rate,%.3f)]?\r\n'%flowrate
    ser.write(message.encode())
    ser.close()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('{} Pumping at {} mL/min'.format(ts, flowrate))

def stop(ser):
    ser.open()
    ser.write('?[1003,0,1,CMD,SYN,0(Stop Pump,false)]?\r\n'.encode())
    ser.close()
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print('{} Pump stopped'.format(ts))

def start_pressure_samples(ser,datapoint_interval):
    message = '?[1003,0,1,CMD,SYN,0(Start pressure samples,{},1)]?\r\n'.format(datapoint_interval)
    ser.open()
    ser.write(message.encode())
    ser.close()
    print('{} Started pressure sampling every {} ms'.format(ts,datapoint_interval))

def stop_pressure_samples(ser):
    ser.open()
    ser.write('?[1003,0,1,CMD,SYN,0(Stop)]?\r\n'.encode())
    ser.close()
    print('{} Stopped pressure sampling'.format(ts))

def read_messages(ser,duration):
    ser.open()
    t0 = time.time()
    t = t0
    while (t-t0) < duration:
        if ser.inWaiting() > 0:
            ser.readline()
    ser.close()

if __name__ == "__main__":
    pump1 = serial.Serial(port='COM9',\
                          baudrate=115200,\
                        # parity=PARITY_NONE,\
                        # bytesize=EIGHTBITS,\
                          dsrdtr=True,\
                          rtscts=True,\
                        # stopbits=STOPBITS_ONE,\
                          timeout=1)
    pump1.close()