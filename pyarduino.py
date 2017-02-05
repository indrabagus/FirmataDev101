import serial
import time


class Utility:
    """
    Merubah payload menjadi string untuk ditulis ke terminal ataupun ke logfile
    kwargs:
        lenblock = [Integer]
            The length of data string in a line
        
        enableaddr = [Boolean True/False]
            Enable the address information on string returned value
            
        startaddr = [Integer] 
            Starting address of the payload
    """
    def payload2str(pdu,**kwargs):
        lenblock=16
        addr = 0x0000
        enaddr = True
    
        if "lenblock" in kwargs:
            if isinstance(kwargs["lenblock"],int) == False:
                raise TypeError("lenblock should be boolean type ( True/False )")
            lenblock=kwargs["lenblock"]
        
        if "startaddr" in kwargs:
            if isinstance(kwargs["startaddr"],int) == False:
                raise TypeError("startaddr should be integer type")    
            addr=kwargs["startaddr"]
    
        if "enableaddr" in kwargs:
            if isinstance(kwargs["enableaddr"],bool) == False:
                raise TypeError("enableaddr should be boolean type ( True/False )")    
            enaddr = kwargs["enableaddr"]
    
        szret = ""
    
        for i in range(len(pdu)//lenblock):
            if(enaddr):
                szret = szret + "%4.4X   : " % addr
            # else:
            #     szret = szret + "| "
            szret = szret + "".join("%2.2X" % c for c in pdu[i*lenblock : (i*lenblock) + lenblock])
            # ingat! ada karakter spasi di operasi join diatas
            # szret = szret + "|" #"|\n"
            addr = addr + lenblock
     
        sisa=len(pdu) % lenblock
        if sisa == 0:
            return szret
        if(enaddr):
            szret = szret + "| %4.4X   " % addr
        # else:
        #     szret = szret + "| "        
        szret = szret + "".join("%2.2X" % c for c in pdu[len(pdu)-sisa : len(pdu)])
        # szret = szret + "".join("." for c in range(lenblock-sisa))         
        # szret = szret + "".join(" . " for c in range(lenblock-sisa)) + "|" #"|\n"
        return szret

    def logcomm(bytesdata,istx=True):
        if(istx):
            sz = "TX: " 
        else:
            sz = "RX: "
        print(sz + Utility.payload2str(bytesdata,enableaddr=False))


class Arduino(object):
    def __init__(self,port,baudrate=57600):
        self.enablelogcom = True
        self._majorfirmware = None
        self._minorfirmware = None
        # Initialization of serial port
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.serial.parity = serial.PARITY_NONE #set parity check: no parity
        self.serial.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.serial.timeout = 2              #timeout block read
        self.serial.xonxoff = False     #disable software flow control
        self.serial.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.serial.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.serial.writeTimeout = 2     #timeout for write        
        self.serial.open()
        self._get_firmware()
        

    def _get_firmware(self):
        datatx = bytes([0xF0,0x79,0xF7])
        Utility.logcomm(datatx)
        self.serial.write(datatx)
        self.serial.flush()
        starttime = time.time()
        while(self.serial.inWaiting() == 0):
            if((time.time() - starttime) > 10):
                raise IOError("Time out during get firmware")
        resp = self.serial.readline()
        Utility.logcomm(resp,False)
        # Validate response, ex resp: F0790205610072006400750069006E006F005F00310030003100F7
        le = len(resp)
        if(le < 5) or
           (resp[0] != 0xF0) or 
           (resp[1] != 0x79) or 
           (resp[le-1] != 0xF7)):
            raise Exception("Invalid firmware response")
        self._majorfirmware = resp[2]
        self._minorfirmware = resp[3]
        # Extract the firmware string (if it exist)
        if(le > 5):
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if(self.serial.isOpen()):
            self.serial.close()
    
    def GetMajorFirmware(self):
        return self._majorfirmware

    def GetMinorFirmware(self):
        return self._minorfirmware


if __name__ == '__main__':
    print("Initiate Arduino board")
    with Arduino('COM4') as board:
        pass
