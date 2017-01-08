from Libraries.RACOM.RACOM_TP import RACOM_TP


class I2C:
    RacomTP = None

    def __init__(self):
        self.RacomTP = RACOM_TP("UART")
        
    def set_I2C_register(self, address, register, value):
        global RacomTP
        data = [address, register, value]
        self.RacomTP.send(0x11, data)
    
    def get_I2C_register(self, address, register):
        global RacomTP
        data = [address, register]
        self.RacomTP.send(0x10, data)
        while self.RacomTP.available() == 0:
            continue
        return self.RacomTP.read()

    def get_I2C_Word(self, address, register):
        global RacomTP
        data = [address, register]
        self.RacomTP.send(0x12, data)
        while self.RacomTP.available() == 0:
            continue
        return self.RacomTP.read()
