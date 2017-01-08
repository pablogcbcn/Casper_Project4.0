from Libraries.RACOM.RACOM_TP import RACOM_TP


class GPIO:
    HIGH = 0x1
    LOW = 0x0
    INPUT = 0x0
    OUTPUT = 0x1
    RacomTP = None

    def __init__(self):
        HIGH = 1
        LOW = 0
        INPUT = 0
        OUTPUT = 1
        self.RacomTP = RACOM_TP("UART")
        
    def set_GPIO_mode(self, pin, mode):
        data = [pin, mode]
        self.RacomTP.send(0x19, data)

    def set_GPIO(self, pin, output):
        self.RacomTP = RACOM_TP("UART")
        data = [pin, output]
        self.RacomTP.send(0x17, data)

    def get_GPIO(self, pin):
        data = [pin]
        self.RacomTP.send(0x16, data)
        while self.RacomTP.available() == 0:
            continue
        return self.RacomTP.read()
