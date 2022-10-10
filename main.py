#Tim Engelbracht, 08.10.22
import serial
import time
import numpy as np
import typing

#TODO: Arbitary-mode


#Python wrapper for serial communication/ remote control of a Rohde & Schwarz (Hameg) HM8143 Arbitrary Power Supply

#Baudrate may be varied. Instructions can be found in the manual (sect. 8.3)

class HM8143():

    def __init__(self, port: str = 'COM5', baudrate: int = 9600):
        # set up serial connection

        if baudrate not in [9600, 19200, 4800]:
            raise ValueError('baudrate not supported')

        self.ser = serial.Serial(port=port,
                                baudrate=baudrate,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout = 0)

    def start_remote_control(self):
        #start remote control and disable physical controls

        self.ser.write('RM1'.encode())

        return 1

    def end_remote_control(self):
        #end remote control and reactivate physical controls

        self.ser.write('RM0'.encode())

        return 1

    def start_mixed_control(self):
        # start mixed control: device can be controlled physically and remotely

        self.ser.write('MX1'.encode())

        return 1

    def end_mixed_control(self):
        # end mixed control: device is set back to remote control

        self.ser.write('MX0'.encode())

        return 1

    def enable_output_sockets(self):
        #turn output sockets on

        self.ser.write('OP1'.encode())

        return 1

    def disable_output_sockets(self):
        #turn output sockets off

        self.ser.write('OP0'.encode())

        return 1

    def set_voltage(self, channel: int = 1, voltage: float = 6.9):
        # set channel voltage (VV.mVmV)

        if channel not in [1,2]:
            raise ValueError('channel index must not exceed 2')

        if voltage > 30.0:
            raise ValueError('voltage must not exceed 30V')

        self.ser.write(f'SU{channel}:{voltage}'.encode())

        return 1

    def set_voltage_sync(self, voltage: float = 6.9):
        #set voltage of both channels synchronously (U1 = U2), TRACKING-mode (VV.mVmV)

        if voltage > 30.0:
            raise ValueError('voltage must not exceed 30V')

        self.ser.write(f'TRU:{voltage}'.encode())

        return 1

    def set_current(self, channel: int = 1, current: float = 0.420):
        # set channel current (A.mAmAmA)

        if channel not in [1,2]:
            raise ValueError('channel index must not exceed 2')

        if current > 2.0:
            raise ValueError('current must not exceed 2A')

        self.ser.write(f'SI{channel}:{current}'.encode())

    def set_current_sync(self, current: float = 0.420):
        # set current of both channels synchronously (I1 = I2), TRACKING-mode (A.mAmAmA)

        if current > 2.0:
            raise ValueError('current must not exceed 30V')

        self.ser.write(f'TRI:{current}'.encode())

        return 1

    def set_fuse(self):
        # activate electronic fuse

        self.ser.write('SF'.encode())

        return 1

    def clear_fuse(self):
        # deactivate electronic fuse

        self.ser.write('CF'.encode())

        return 1

    def return_voltage_target(self, channel: int = 1):
        #return TARGET voltage value (RUx)

        self.ser.write(f'RU{channel}'.encode())

        return self.ser.readline().decode()

    def return_current_target(self, channel: int = 1):
        #return TARGET current value (RIx)

        self.ser.write(f'RI{channel}'.encode())

        return self.ser.readline().decode()

    def return_voltage_actual(self, channel: int = 1):
        #return ACTUAL voltage value (MUx)

        self.ser.write(f'MU{channel}'.encode())

        return self.ser.readline().decode()

    def return_current_actual(self, channel: int = 1):
        #return ACTUAL current value (MIx)

        self.ser.write(f'MI{channel}'.encode())

        return self.ser.readline().decode()

    def return_status(self):
        #return device status

        self.ser.write('STA'.encode())

        return self.ser.readline().decode()

    def return_version(self):
        #return the device's software version

        self.ser.write('VER'.encode())

        return self.ser.readline().decode()

    def return_ID(self):
        #return the device's ID

        self.ser.write('ID?'.encode())

        return self.ser.readline().decode()

    def clear(self):
        # disable output sockets, set all currents and voltages to zero
        #TRACKING-mode and fuse not affected

        self.ser.write('CLR'.encode())

        return 1

    def load_arbitrary_func(self, arb_function: typing.Dict[float, float], iteration: int):
        #loads arbitrary func as dict {duration1: voltage1, duration2: voltage2, ...}
        #example: arb_function = {1: 20.0, 1e-3: 15.0, 100e-3: 2.0}
        #if iteration = 0: endless looping through arb func

        #TODO: testing of arb func

        comm = 'ABT:'

        if iteration > 255:
            raise ValueError('max iterations: 255')

        if len([vals for vals in arb_function.items() if vals[1] > 30]) > 0:
            raise ValueError('voltages must not exceed 30V')


        #time in seconds: serial key
        time_mapping = {100e-6: '0',
                        1e-3: '1',
                        2e-3: '2',
                        5e-3: '3',
                        10e-3: '4',
                        20e-3: '5',
                        50e-3: '6',
                        100e-3: '7',
                        200e-3: '8',
                        50e-3: '9',
                        1: 'A',
                        2: 'B',
                        5: 'C',
                        10: 'D',
                        20: 'E',
                        50: 'F'}

        if set(list(arb_function.keys())).issubset(set(list(time_mapping.keys()))) == False:
            raise ValueError('one of the set durations in arb func is not suppoerted. Choose from the following: [0.05, 0.1, 0.2, 1, 2, 5, 10, 0.01, 50, 20, 0.005, 0.02, 0.0001, 0.002, 0.001]')
        #

        for key in arb_function:
            comm = comm + time_mapping[key] + f"{arb_function[key]:05.2f}" + '_'

        comm = comm + f"N{iteration}"

        self.ser.write(comm.encode())

        return 1

    def run_arbitrary_func(self):
        #run the loaded arbitrary function

        self.ser.write('OP1'.encode())
        time.sleep(0.1)
        self.ser.write('RUN'.encode())

        return 1

    def stop_arbitrary_func(self):
        # stop the running arbitrary function

        self.ser.write('STP'.encode())
        time.sleep(0.1)
        self.ser.write('OP0'.encode())

        return 1

    def end_connection(self):

        self.ser.close()

        return 1






if __name__ == '__main__':

    dev = HM8143()
    dev.return_ID()
    dev.start_remote_control()

    # for i in np.linspace(1,29,29):
    #
    #     dev.set_voltage_sync(i*1)
    #     time.sleep(0.05)
    #     print(dev.return_current_target(1))
    #     time.sleep(0.05)
    #dev.set_current(1,0.420)

    time.sleep(1)
    print(dev.return_status())
    time.sleep(1)

    dev.load_arbitrary_func({1: 20.0, 1e-3: 15.0, 100e-3: 2.0}, 2)
    dev.run_arbitrary_func()

    a = 0
    while a<3:
        print(dev.return_voltage_actual(2))
        time.sleep(0.1)
        a = a + 0.1

    #dev.end_remote_control()
    dev.clear()
    time.sleep(1)
    dev.end_connection()

    a = 2