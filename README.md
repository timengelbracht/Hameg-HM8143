# Python Wrapper for Rhode & Schwarz (Hameg) - HM8143

## Description
    This Python wrapper allows for easy communication with the R&S (Hameg) HM8143 Power Supply Unit via Python's PySerial API.
    The main goal of this project is to automize electrical lab work dealing with varying voltages and currents, which normally would have
    been done by manually setting the power supply unit.

## Installation
    1. Install the current device driver. It can be found at the manufactures website (https://www.rohde-schwarz.com/de/treiber/hm8143/). Supported OS: Windows XP, Vista, 7, 8, 10 (32-/64-bit)
    
## Use
    1. Figure out, through which COM port the serial connection will be made
    2. Instantiate an HM8143 object. This will establish the connection with the device
    3. **Do your stuff**
    4. close the connection

## Example

        ´´´
        #instantiate object, thus opening connection
        dev = HM8143(port="COM5")

        #start remote control
        dev.start_remote_control()

        #set voltages und currents
        for i in np.linspace(1, 30, 30):
    
            dev.set_voltage(i, 1)
            time.sleep(0.01)
    
            dev.set_current(i*0.06, 1)
            time.sleep(0.01)
    
            dev.set_voltage(30-i, 2)
            time.sleep(0.01)
    
            dev.set_current(2-(i*0.06), 2)
            time.sleep(0.01)
        
        time.sleep(1)
        #end remote control
        dev.end_remote_control()
    
        time.sleep(1)
        #close serial connection
        dev.end_connection()
        ´´´
## More infos
    functionalities exceed what is shown in the example. Further functions include: 
        - mixed mode (both manual and remote control)
        - synchronized mode (both channels synchronized)
        - arbitrary mode (load a series of duration/voltage pairs as a dictinary, which will be set succcessively and repeatedly)
        - several supplementary info returns (device status, software version,...)
    For more information be sure to look at the comments in the code and the manual (german/english), which can be found on the manufacturers website (https://www.rohde-schwarz.com/de/handbuch/hm8143-three-channel-arbitrary-power-supply-benutzerhandbuch-handbuecher-gb1_78701-157000.html)
