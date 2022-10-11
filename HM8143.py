#!/usr/bin/env python3
__author__ = 'Tim Engelbracht'
__email__ = "engelbracht@imr.uni-hannover.de"
__status__ = "Development"

import serial
import numpy as np
import time
import typing
import logging

# TODO: Arbitary-mode


# Python wrapper for serial communication/ remote control of a Rohde & Schwarz (Hameg) HM8143 Arbitrary Power Supply

# Baudrate may be varied. Instructions can be found in the manual (sect. 8.3)

LOGGING_LEVEL = None


class HM8143():
    # time in seconds: serial key
    TIME_MAPPING = {100e-6: '0',
                    1e-3: '1',
                    2e-3: '2',
                    5e-3: '3',
                    10e-3: '4',
                    20e-3: '5',
                    50e-3: '6',
                    100e-3: '7',
                    200e-3: '8',
                    500e-3: '9',
                    1: 'A',
                    2: 'B',
                    5: 'C',
                    10: 'D',
                    20: 'E',
                    50: 'F'}

    def __init__(self, port: str, baudrate: int = 9600):
        self.logger = logging.getLogger(__name__)
        if LOGGING_LEVEL is not None:
            self.logger.setLevel(LOGGING_LEVEL)

        # set up serial connection
        if baudrate not in [4800, 9600, 19200]:
            raise ValueError('Baudrate not supported')

        self.logger.debug(f"Trying to establish serial connection on port: {port}")
        self.ser = serial.Serial(port=port,
                                 baudrate=baudrate,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS,
                                 timeout=0)

    def _serial_encode(self, cmd: str):
        """
        encode the command into byte data

        Parameters
        ----------
        cmd: str
            command sent to the device

        Returns
        -------
        cmd, byte encoded
        """
        return cmd.encode()

    def _serial_decode(self, ret: bytes):
        """
        decode the return from byte data

        Parameters
        ----------
        cmd: byte str
            return received from the device

        Returns
        -------
        cmd, decoded
        """
        return ret.decode()

    def start_remote_control(self):
        """
        Start remote control and disable physical controls

        """
        self.ser.write(self._serial_encode('RM1'))

    def end_remote_control(self):
        """
        end remote control and reactivate physical controls

        """
        self.ser.write(self._serial_encode('RM0'))

    def start_mixed_control(self):
        """
        start mixed control: device can be controlled physically and remotely

        """
        self.ser.write(self._serial_encode('MX1'))

    def end_mixed_control(self):
        """
        end mixed control: device is set back to remote control

        """
        self.ser.write(self._serial_encode('MX0'))

    def enable_output_sockets(self):
        """
        turn output sockets on

        """
        self.ser.write(self._serial_encode('OP1'))

    def disable_output_sockets(self):
        """
        turn output sockets off

        """
        self.ser.write(self._serial_encode('OP1'))

    def set_voltage(self, voltage: float, channel: int = 1):
        """
        set channel voltage

        Parameters
        ----------
        voltage: float
            voltage to be set, format: VV.mVmV, must not exceed 30 Volts

        channel: int
            channel for which the voltage is set, must not exceed 2

        """
        if channel not in [1, 2]:
            raise ValueError('channel index must not exceed 2')

        if voltage > 30.0:
            raise ValueError('voltage must not exceed 30V')

        self.ser.write(self._serial_encode(f'SU{channel}:{voltage}'))

    def set_voltage_sync(self, voltage: float):
        """
        set voltage of both channels synchronously (U1 = U2), TRACKING-mode

        Parameters
        ----------
        voltage: float
            voltage to be set, format: VV.mVmV, must not exceed 30 Volts

        """
        if voltage > 30.0:
            raise ValueError('voltage must not exceed 30V')

        self.ser.write(self._serial_encode(f'TRU:{voltage}'))

    def set_current(self, current: float, channel: int = 1):
        """
        set channel current (A.mAmAmA)

        Parameters
        ----------
        current: float
            current to be set, format: A.mAmAmA, must not exceed 2 Ampere

        channel: int
            channel for which the current is set, must not exceed 2

        """

        if channel not in [1, 2]:
            raise ValueError('channel index must not exceed 2')

        if current > 2.0:
            raise ValueError('current must not exceed 2A')

        self.ser.write(self._serial_encode(f'SI{channel}:{current}'))

    def set_current_sync(self, current: float):
        """
        set current of both channels synchronously (I1 = I2), TRACKING-mode (A.mAmAmA)

        Parameters
        ----------
        current: float
            current to be set, format: A.mAmAmA, must not exceed 2 Ampere
        """
        if current > 2.0:
            raise ValueError('current must not exceed 30V')

        self.ser.write(self._serial_encode(f'TRI:{current}'))

    def set_fuse(self):
        """
        activate electronic fuse

        """

        self.ser.write(self._serial_encode('SF'))

    def clear_fuse(self):
        """
        deactivate electronic fuse

        """

        self.ser.write(self._serial_encode('CF'))

    def return_voltage_target(self, channel: int = 1):
        """
        return TARGET voltage value (RUx)

        Parameters
        ----------
        channel: int
            channel for which the voltage is set, must not exceed 2

        Returns
        -------
        target voltage: str
        """

        self.ser.write(self._serial_encode(f'RU{channel}'))

        return self._serial_decode(self.ser.readline())

    def return_current_target(self, channel: int = 1):
        """
        return TARGET current value (RIx)

        Parameters
        ----------
        channel: int
            channel for which the current is set, must not exceed 2

        Returns
        -------
        target current: str
        """
        self.ser.write(self._serial_encode(f'RI{channel}'))

        return self._serial_decode(self.ser.readline())

    def return_voltage_actual(self, channel: int = 1):
        """
        return ACTUAL voltage value (MUx)

        Parameters
        ----------
        channel: int
            channel for which the voltage is set, must not exceed 2

        Returns
        -------
        actual voltage: str
        """

        self.ser.write(self._serial_encode(f'MU{channel}'))

        return self._serial_decode(self.ser.readline())

    def return_current_actual(self, channel: int = 1):
        """
        return ACTUAL current value (MIx)

        Parameters
        ----------
        channel: int
            channel for which the voltage is set, must not exceed 2

        Returns
        -------
        actual current: str
        """

        self.ser.write(self._serial_encode(f'MI{channel}'))

        return self._serial_decode(self.ser.readline())

    def return_status(self):
        """
        return device status

        Returns
        -------
        status: str
        """

        self.ser.write(self._serial_encode('STA'))

        return self._serial_decode(self.ser.readline())

    def return_version(self):
        """
        return device's software version

        Returns
        -------
        version: str
        """

        self.ser.write(self._serial_encode('VER'))

        return self._serial_decode(self.ser.readline())

    def return_ID(self):
        """
        return device ID

        Returns
        -------
        ID: str
        """

        self.ser.write(self._serial_encode('ID?'))

        return self._serial_decode(self.ser.readline())

    def clear(self):
        """
        disable output sockets, set all currents and voltages to zero
        TRACKING-mode and fuse not affected

        """

        self.ser.write(self._serial_encode('CLR'))

    def load_arbitrary_func(self, arb_function: typing.Dict[float, float], iteration: int):
        """
        loads arbitrary func as dict {duration1: voltage1, duration2: voltage2, ...}

        if iteration = 0: endless looping through arb func

        Parameters
        ----------
        arb_function: dict
            arbitrary function containing duration (seconds) and voltage (volts) pairs to be executed
            example: arb_function = {1: 20.0, 1e-3: 15.0, 100e-3: 2.0}

        iteration: int
            number of arbitrary function calls
        """

        comm = 'ABT:'

        if iteration > 255:
            raise ValueError('max iterations: 255')

        if len([vals for vals in arb_function.items() if vals[1] > 30]) > 0:
            raise ValueError('voltages must not exceed 30V')

        if not set(list(arb_function.keys())).issubset(set(list(self.TIME_MAPPING.keys()))):
            raise ValueError('one of the set durations in arb func is not supported. Choose from the following: '
                             '[0.05, 0.1, 0.2, 1, 2, 5, 10, 0.01, 50, 20, 0.005, 0.02, 0.0001, 0.002, 0.001]')

        for key in arb_function:
            comm = comm + self.TIME_MAPPING[key] + f"{arb_function[key]:05.2f}" + '_'

        comm = comm + f"N{iteration}"

        self.ser.write(self._serial_encode(comm))

    def run_arbitrary_func(self):
        """
        run the loaded arbitrary function

        """

        self.ser.write(self._serial_encode('OP1'))
        time.sleep(0.1)
        self.ser.write(self._serial_encode('RUN'))

    def stop_arbitrary_func(self):
        """
        stop the running arbitrary function

        """

        self.ser.write(self._serial_encode('STP'))
        time.sleep(0.1)
        self.ser.write(self._serial_encode('OP0'))

    def end_connection(self):
        """
        end serial connection with the device

        """
        self.ser.close()


if __name__ == '__main__':

    dev = HM8143(port="COM5")
    dev.return_ID()
    dev.start_remote_control()

    # i = 1
    # try:
    #     while True:
    #         if i < 30:
    #             dev.set_voltage(i, 1)
    #             time.sleep(0.05)
    #
    #             dev.set_current(i * 0.06, 1)
    #             time.sleep(0.05)
    #
    #             dev.set_voltage(30 - i, 2)
    #             time.sleep(0.05)
    #
    #             dev.set_current(2 - (i * 0.06), 2)
    #             time.sleep(0.05)
    #
    #             i = i + 1
    #         else:
    #             i = 1
    # except KeyboardInterrupt:
    #     pass

    for i in np.linspace(1, 30, 30):

        dev.set_voltage(i, 1)
        time.sleep(0.1)

        dev.set_current(i*0.06, 1)
        time.sleep(0.1)

        dev.set_voltage(30-i, 2)
        time.sleep(0.1)

        dev.set_current(2-(i*0.06), 2)
        time.sleep(0.1)

    time.sleep(1)

    dev.end_remote_control()

    time.sleep(1)
    dev.end_connection()

    a = 2
