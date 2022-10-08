#Tim Engelbracht, 08.10.22
import serial
import time

#TODO: was hat es mit dem 3. Kanal auf sich?
#TODO: returns
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
                                bytesize=serial.EIGHTBITS)

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
        pass

    def return_current_target(self, channel: int = 1):
        #return TARGET current value (RIx)
        pass

    def return_voltage_actual(self, channel: int = 1):
        #return ACTUAL voltage value (MUx)
        pass

    def return_current_actual(self, channel: int = 1):
        #return ACTUAL current value (MIx)
        pass

    def return_status(self):
        #return device status
        pass

    def return_version(self):
        #return the device's software version
        pass

    def return_ID(self):
        #return the device's ID
        pass

    def clear(self):
        # disable output sockets, set all currents and voltages to zero
        #TRACKING-mode and fuse not affected

        self.ser.write('CLR'.encode())

        return 1






if __name__ == '__main__':
    ser = serial.Serial(
        port='COM5',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )



    ser.write('RM0'.encode())
    time.sleep(1)
    ser.write('RM1'.encode())
    time.sleep(1)
    for i in range(20):
        ser.write(f'OP1'.encode())
        time.sleep(0.1)
        ser.write(f'SU1:{str(i)}.00'.encode())
        time.sleep(1)
